import time
from datetime import datetime, timezone
import sys
import importlib.metadata

import click

from tensorkube.constants import ADDON_NAME, REGION, Events, DEFAULT_NAMESPACE, get_cluster_name, CliColors
from tensorkube.constants import get_mount_driver_role_name, get_mount_policy_name, get_base_login_url
from tensorkube.helpers import create_mountpoint_driver_role_with_policy, sanitise_assumed_role_arn, track_event, \
    sanitise_name
from tensorkube.migration_service.migration_manager.migration_service import set_current_cli_version_to_cluster, \
    migrate_tensorkube
from tensorkube.services.aws_service import get_aws_account_id, get_credentials, get_bucket_name, get_aws_user_arn, \
    get_aws_user_principal_arn, get_session_region
from tensorkube.services.cloudformation_service import delete_cloudformation_stack, delete_launch_templates, \
    cloudformation, get_validation_records_from_events, get_validation_records_with_wait
from tensorkube.services.dataset_service import upload_tensorkube_dataset, delete_tensorkube_dataset
from tensorkube.services.deploy import Config, deploy_knative_service, DEFAULT_GPUS, DEFAULT_CPU, DEFAULT_MEMORY, \
    DEFAULT_MIN_SCALE, DEFAULT_MAX_SCALE, DEFAULT_ENV, DEFAULT_SECRET, build_app, create_deployment_details
from tensorkube.services.dynamodb_service import get_all_job_statuses, get_job_statuses
from tensorkube.services.ecr_service import delete_all_tensorkube_ecr_repositories
from tensorkube.services.eks_service import install_karpenter, apply_knative_crds, apply_knative_core, \
    delete_knative_crds, delete_knative_core, delete_karpenter_from_cluster, apply_nvidia_plugin, create_eks_addon, \
    delete_eks_addon, update_eks_kubeconfig, give_eks_cluster_access
from tensorkube.services.eksctl_service import create_base_tensorkube_cluster_eksctl, delete_cluster
from tensorkube.services.environment_service import create_new_environment, list_environments, delete_environment
from tensorkube.services.filesystem_service import cleanup_filesystem_resources, configure_efs
from tensorkube.services.iam_service import create_iam_user, create_eks_access_policy, attach_policy_to_user, \
    create_access_key, create_user_sqs_access_policy, create_user_s3_access_policy, create_user_dynamo_access_policy
from tensorkube.services.iam_service import create_mountpoint_iam_policy, detach_role_policy, delete_role, delete_policy
from tensorkube.services.istio import check_and_install_istioctl, install_istio_on_cluster, install_net_istio, \
    install_default_domain, remove_domain_server, uninstall_istio_from_cluster
from tensorkube.services.job_queue_service import deploy_job, create_cloud_resources_for_queued_job_support, queue_job, \
    get_job_status, delete_all_job_resources, teardown_job_queue_support, is_existing_queued_job, \
    create_sa_role_rb_for_job_sidecar
from tensorkube.services.k8s_service import create_aws_secret, create_build_pv_and_pvc, create_secret, list_secrets, \
    delete_secret, list_keda_scaled_jobs, add_user_to_k8s
from tensorkube.services.karpenter_service import apply_karpenter_configuration
from tensorkube.services.knative_service import enable_knative_selectors_pv_pvc_capabilities, cleanup_knative_resources, \
    delete_knative_services
from tensorkube.services.local_service import check_and_install_cli_tools
from tensorkube.services.logging_service import configure_cloudwatch, teardown_cloudwatch
from tensorkube.services.metapod_service import list_instances_in_cloud, start_devcontainer, purge_devcontainer, \
    pause_devcontainer, reset_cloud
from tensorkube.services.rich_service import list_tensorkube_deployments, describe_deployment, display_deployment_logs, \
    ssh_into_deployed_service, display_secrets, list_tensorkube_datasets, display_job_logs, \
    delete_tensorkube_job_by_prefix, list_tensorkube_training_jobs, display_queued_jobs, get_tensorkube_training_job, \
    prettify_aws_user_keys, display_specific_queued_job, display_dns_records_table, delete_deployment
from tensorkube.services.s3_access_service import create_s3_access_to_pods
from tensorkube.services.s3_service import create_s3_bucket, delete_s3_bucket
from tensorkube.services.tls_service import configure_certificate, get_certificate_stack_name, attach_domain_name, \
    validate_domain, check_if_a_domain_is_validated
from tensorkube.services.train import axolotl_train, get_job_prefix_from_job_id
from tensorkube.tensorkube_token_server import run_server

from tensorkube.services.nydus import get_nydus_image_url, install_nydus, delete_nydus

from tensorkube.services.ecr_service import get_or_create_ecr_repository
from tensorkube.services.version_service import print_tensorkube_version
from tensorkube.services.build import configure_buildkit_irsa, delete_buildkit_irsa

@click.group()
@click.pass_context
def tensorkube(ctx):
    args = sys.argv
    full_command = ""
    subcommand = ctx.invoked_subcommand
    if subcommand:
        if len(args) > 1:
            for arg in args[1:]:
                if arg.startswith("--"):
                    if subcommand == "dev" and arg == "--cloud":
                        full_command += arg + " "
                    else:
                        break
                elif subcommand == "secret" and (arg == "create" or arg == "delete"):
                        full_command += arg + " "
                        break
                else:
                    full_command += arg + " "

        track_event(Events.COMMAND_RUN.value, {"command": full_command,
                                               "tensorkube_version": importlib.metadata.version("tensorkube")})

    pass


@tensorkube.group()
def list():
    """
    List Tensorkube apps that are currently deployed.
    """
    pass


@tensorkube.group()
def secret():
    """Create, list, and delete secrets."""
    pass


@list.command()
@click.option('--env', default=None, type=str, help='Environment to list the services from.')
@click.option('--all', is_flag=True, help='List all services from all environments.')
@click.option('--old', is_flag=True, help='List older sslip urls for using as hosts if you are on an older version.')
def deployments(env, all, old):
    list_tensorkube_deployments(env_name=env, all=all, old=old)


@list.command()
@click.option('--env', default=DEFAULT_NAMESPACE, type=str, help='Environment to list the secrets from.')
def secrets(env):
    secrets = list_secrets(env)
    if not secrets:
        if env == DEFAULT_NAMESPACE:
            click.echo("No secrets found")
        else:
            click.echo(f"No secrets found in environment " + click.style(env, bold=True))
        return
    display_secrets(secrets, env)


@tensorkube.command()
def install_prerequisites():
    """Install all the prerequisites required to run Tensorfuse on a local machine."""
    check_and_install_cli_tools()


@tensorkube.command()
def upgrade():
    """Migrate your tensorfuse cluster to the latest version of tensorkube.

    This command automatically takes all the necessary actions to upgrade the software that is  managing your Tensorfuse cluster.
    """
    migrate_tensorkube()


@tensorkube.command()
@click.option('--vpc-public-subnets', type=str, help='[Experimental] List of public subnets should be given if you want to create in existing VPC. If not given, a new VPC will be created. You should ignore this flag unless you want to create cluster in existing vpc. Tensorfuse recommends to create a new vpc for the tensorkube cluster instead of deploying in existing vpc. This is a enterprise feature. Reach out to tensorfuse for more information.')
@click.option('--vpc-private-subnets', type=str, help='[Experimental] List of private subnets should be given if you want to create in existing VPC. If not given, a new VPC will be created.You should ignore this flag unless you want to create cluster in existing vpc. Tensorfuse recommends to create a new vpc for the tensorkube cluster instead of deploying in existing vpc. This is a enterprise feature. Reach out to tensorfuse for more information.')
def configure(vpc_public_subnets, vpc_private_subnets):
    """Configure the Tensorkube runtime on your private cloud
    """
    click.echo("Configuring the Tensorfuse runtime for your cloud...")
    start_time = time.time() * 1000
    can_track = track_event(Events.CONFIGURE_START.value, {"start_time": start_time})
    if not can_track:
        click.echo("You need to login to Tensorfuse to configure Tensorkube.")
        click.echo("Please login using the command: " + click.style("tensorkube login", fg='cyan'))
        return
    confirmation_txt = click.style("Confirmation: Tensorfuse sets up resources such as a Kubernetes cluster, load balancer, and cluster autoscaler to enable serverless GPUs and features like job queues. The estimated base cost for this setup is approximately ") + click.style("$300 per month", bold=True) + click.style(", billed by AWS. Please select \"Yes\" if you wish to proceed.")
    confirmation = click.confirm(confirmation_txt, default=False)
    if not confirmation:
        end_time = time.time() * 1000
        track_event(Events.CONFIGURE_END.value,
                {"start_time": start_time, "end_time": end_time, "duration": end_time - start_time, "status": "confirmation_declined"})    
        return
    session_region = get_session_region()
    if session_region != REGION:
        end_time = time.time() * 1000
        track_event(Events.CONFIGURE_END.value,
                {"start_time": start_time, "end_time": end_time, "duration": end_time - start_time, "status": "region_not_supported", "region": session_region})    
        click.echo(click.style( f"Error: The current region is {session_region}. Tensorfuse currently supports only {REGION} region. Either switch your region to {REGION} or reach out to ", bold=True,
                        fg=CliColors.ERROR.value) + click.style( "founders@tensorfuse.io", italic=True, bold=True, fg=CliColors.ERROR.value) + click.style(" for support.", bold=True, fg=CliColors.ERROR.value))
        return
    
    if not check_and_install_cli_tools():
        return
    # TODO!: add helm annotations

    # create cloudformation stack
    cloudformation()
    
    # create eks cluster
    vpc_public_subnets_list = vpc_public_subnets.split(",") if vpc_public_subnets else []
    vpc_private_subnets_list = vpc_private_subnets.split(",") if vpc_private_subnets else []
    create_base_tensorkube_cluster_eksctl(cluster_name=get_cluster_name(), vpc_public_subnets=vpc_public_subnets_list, vpc_private_subnets=vpc_private_subnets_list)
    # install karpenter
    install_karpenter()
    # # apply karpenter configuration
    apply_karpenter_configuration()
    configure_cloudwatch()
    #
    # install istio networking plane
    check_and_install_istioctl()
    install_istio_on_cluster()

    # install knative crds
    apply_knative_crds()
    # install knative core
    apply_knative_core()

    # install nvidia plugin
    apply_nvidia_plugin()
    #
    # install net istio
    install_net_istio()

    # create s3 bucket for build
    bucket_name = get_bucket_name()
    create_s3_bucket(bucket_name)

    

    # create mountpoint policy to mount bucket to eks cluster
    create_mountpoint_iam_policy(get_mount_policy_name(get_cluster_name()), bucket_name)

    # create s3 csi driver role and attach mountpoint policy to it
    create_mountpoint_driver_role_with_policy(cluster_name=get_cluster_name(), account_no=get_aws_account_id(),
                                              role_name=get_mount_driver_role_name(get_cluster_name()),
                                              policy_name=get_mount_policy_name(get_cluster_name()))

    # create eks addon to mount s3 bucket to eks cluster
    create_eks_addon(get_cluster_name(), ADDON_NAME, get_aws_account_id(),
                     get_mount_driver_role_name(get_cluster_name()))

    # create aws credentials cluster secret
    # TODO!: figure out how to update credentials in case of token expiry
    create_aws_secret(get_credentials())

    # create pv and pvc claims for build
    create_build_pv_and_pvc(bucket_name)

    # update knative to use pod labels
    enable_knative_selectors_pv_pvc_capabilities()

    # enable Network files system for the cluster
    click.echo("Configuring EFS for the cluster...")
    configure_efs()

    create_s3_access_to_pods()

    # install keda, create related resources
    create_cloud_resources_for_queued_job_support()
    create_sa_role_rb_for_job_sidecar()
    
    # configure buildkit irsa, so that pods can access ecr
    configure_buildkit_irsa()

    install_nydus()

    # set current cli version to the cluster
    set_current_cli_version_to_cluster()

    end_time = time.time() * 1000

    track_event(Events.CONFIGURE_END.value,
                {"start_time": start_time, "end_time": end_time, "duration": end_time - start_time})
    click.echo("Your tensorfuse cluster is ready and you are good to go.")


@tensorkube.command()
def account():
    """Get the AWS account ID."""
    click.echo(get_aws_account_id())


@tensorkube.command()
def cluster():
    """Get the current cluster name."""
    click.echo(get_cluster_name())


# The following commands can tear down all the resources that you have created and configured using the CLI.

# uninstall knative
# uninstall istio
# uninstall karpenter
# delete cluster

@tensorkube.command()
def teardown():
    """
    HIGHLY DESTRUCTIVE ACTION!!!! Don't run this command if you don't intend to delete all the resources that you have created and configured using the CLI.

    <Warning>
    This action will remove everything you configured using tensorkube.
    </Warning>
    :return:
    """
    start_time = time.time() * 1000
    track_event(Events.TEARDOWN_START.value, {"start_time": start_time})

    # ask for the secret phrase before tearing down and inform the user this means that you are destroying all the resources
    confirmation = click.confirm(click.style("Are you sure you want to tear down all resources? This will destroy all the resources that you have created and configured using Tensorfuse.", bold=True, fg=CliColors.ERROR.value), default=False)
    if not confirmation:
        click.echo("Tear down aborted.")
        return
    else:
        # ask for  a secret phrase if given secret phrase is not correct then abort the teardown
        secret_phrase = click.prompt(click.style("After this action you will no longer be able to use Tensorfuse. Please enter `accept` to confirm the teardown. ", bold=True,fg=CliColors.ERROR.value), hide_input=True)
        if secret_phrase == 'accept':
            click.echo("Tear down confirmed.")
        else:
            click.echo("Phrase is incorrect. Tear down aborted.")
            return

    click.echo("Tearing down all resources...")

    # TODO?: add logic to delete any other resources
    click.echo("Deleting all ECR repositories...")
    delete_all_tensorkube_ecr_repositories()

    click.echo("Deleting all job queue resources...")
    try:
        teardown_job_queue_support()
    except Exception as e:
        click.echo(f"Error while deleting job queue resources: {e}")

    # delete all services
    try:
        delete_knative_services()
    except Exception as e:
        click.echo("Error while deleting Knative services.")
    try:
        cleanup_filesystem_resources()
    except Exception as e:
        click.echo(f"Error while cleaning up filesystem resources: {e}")

    # EKS addon
    try:
        click.echo("Deleting EKS addon...")
        delete_eks_addon(get_cluster_name(), ADDON_NAME)
    except Exception as e:
        click.echo(f"Error while deleting EKS addon: {e}")

    # teardown cloudwatch
    try:
        teardown_cloudwatch()
    except Exception as e:
        click.echo(f"Error while tearing down Cloudwatch: {e}")

    click.echo("Deleting Enviroments...")
    try:
        environments = list_environments()
        for env in environments:
            click.echo(f"Deleting environment: {env}")
            delete_environment(env_name=env)
    except Exception as e:
        click.echo(f"Error while deleting environments: {e}")

    # Detach policy from role, delete role, delete policy
    click.echo("Deleting mountpoint driver role and policy...")
    click.echo("Detaching policy from role...")
    try:
        detach_role_policy(get_aws_account_id(), get_mount_driver_role_name(get_cluster_name()),
                           get_mount_policy_name(get_cluster_name()))
        click.echo("Deleting role...")
        delete_role(get_mount_driver_role_name(get_cluster_name()))
        click.echo("Deleting policy...")
        delete_policy(get_aws_account_id(), get_mount_policy_name(get_cluster_name()))
    except Exception as e:
        click.echo(f"Error while deleting role and policy: {e}")

    # delete s3 bucket
    click.echo("Deleting S3 bucket...")
    try:
        delete_s3_bucket(get_bucket_name())
    except Exception as e:
        click.echo(f"Error while deleting S3 bucket: {e}")

    
    click.echo("Deleting buildkit irsa...")
    try:
        delete_buildkit_irsa()
    except Exception as e:
        click.echo(f"Error while deleting buildkit irsa: {e}")
    
    click.echo("Uninstalling nydus helm charts...")
    try:
        delete_nydus()
    except Exception as e:
        click.echo(f"Error while uninstalling nydus resources: {e}")
    
    click.echo("Uninstalling domain server...")
    try:
        remove_domain_server()
    except Exception as e:
        click.echo(f"Error while uninstalling domain server: {e}")

    click.echo("Uninstalling Knative resources")
    try:
        cleanup_knative_resources()
    except Exception as e:
        click.echo(f"Error while cleaning up Knative resources: {e}")

    click.echo("Uninstalling and deleting Istio resources")
    try:
        uninstall_istio_from_cluster()
    except Exception as e:
        click.echo(f"Error while uninstalling Istio: {e}")
    click.echo("Uninstalling Knative core")
    try:
        delete_knative_core()
        click.echo("Uninstalling Knative CRDs")
        delete_knative_crds()
        click.echo("Successfully uninstalled Knative and Istio.")
    except Exception as e:
        click.echo(f"Error while uninstalling Knative: {e}")

    # remove karpenter
    click.echo("Uninstalling Karpenter...")
    try:
        delete_karpenter_from_cluster()
        click.echo("Successfully uninstalled Karpenter.")
    except Exception as e:
        click.echo(f"Error while uninstalling Karpenter: {e}")
    # delete cluster
    try:
        click.echo("Deleting cluster...")
        delete_cluster()
        click.echo("Successfully deleted cluster.")
    except Exception as e:
        click.echo(f"Error while deleting cluster.: {e}")
    try:
        # delete cloudformation stack
        click.echo("Deleting cloudformation stack...")
        delete_cloudformation_stack(get_cluster_name())
        click.echo("Successfully deleted cloudformation stack.")
    except Exception as e:
        click.echo(f"Error while deleting cloudformation stack: {e}")

    # delete launch templates
    click.echo("Deleting launch templates...")
    delete_launch_templates()

    end_time = time.time() * 1000
    track_event(Events.TEARDOWN_END.value,
                {"start_time": start_time, "end_time": end_time, "duration": end_time - start_time})

    click.echo("Successfully deleted launch templates.")
    click.echo("Tensorfuse has been successfully disconnected from your cluster.")


@tensorkube.command()
@click.option('--gpus', default=DEFAULT_GPUS, help='Number of GPUs needed for the service.')
@click.option('--gpu-type', type=click.Choice(['V100', 'A10G', 'T4', 'L4', 'L40S','A100','H100'], case_sensitive=False),
              help='Type of GPU.')
@click.option('--cpu', type=float, default=DEFAULT_CPU, help='Number of CPU millicores. 1000 = 1 CPU')
@click.option('--memory', type=float, default=DEFAULT_MEMORY, help='Amount of RAM in megabytes.')
@click.option('--min-scale', type=int, default=DEFAULT_MIN_SCALE, help='Minimum number of pods to run.')
@click.option('--max-scale', type=int, default=DEFAULT_MAX_SCALE, help='Maximum number of pods to run.')
@click.option('--env', default=DEFAULT_ENV, type=str, help='Environment to deploy the service to.')
@click.option('--github-actions', is_flag=True, help='Deploying from Github Actions.')
@click.option('--secret', default=DEFAULT_SECRET, type=str, multiple=True, help='Secret to use for the deployment.')
@click.option("--efs", is_flag = True, help="Flag to use EFS for the deployment.")
@click.option('--concurrency', type=int, default=100, help='Number of concurrent requests for a single pod to handle at a time. Pods Scale between min and max scale.')
@click.option('--config-file', type=str,
              help='Path to the config.yaml file. you can use this file instead of cli flags. Keys in config.yaml take precedence than cli flags.')
@click.option('--domain-name', type=str, default=None, help='Domain to use for the deployment.')
@click.option('--port', type=int, default=80, help='Port to expose the service on.')
def deploy(gpus, gpu_type, cpu, memory, min_scale, max_scale, env, github_actions, secret, efs, concurrency, config_file, domain_name, port):
    """
    Deploy your containerized application on Tensorkube. This command requires
    a dockerfile to be present in the current directory.
    """
    click.echo('Preparing configurations for deployment...')
    if env == "default":
        env = DEFAULT_ENV
    try:
        config = Config(config_file)
    except Exception as e:
        click.echo(f"Failed to read config.yaml file: {e}")
        return

    config.set_if_not_exist('gpus', gpus).set_if_not_exist('gpu_type', gpu_type).set_if_not_exist('cpu',
                                                                                                  cpu).set_if_not_exist(
        'memory', memory).set_if_not_exist('min_scale', min_scale).set_if_not_exist('max_scale',
                                                                                    max_scale).set_if_not_exist('env',
                                                                                                                env).set_if_not_exist(
        'github_actions', github_actions).set_if_not_exist('secret', secret).set_if_not_exist('domain', domain_name).set_if_not_exist('efs', efs).set_if_not_exist('concurrency', concurrency).set_if_not_exist('port', port)

    # flags validation
    if config.get('gpus') > 0:
        if not config.get('gpu_type'):
            click.echo(click.style("Error: GPU type is required when GPUs are specified.", fg=CliColors.ERROR.value))
            return
    # TODO add domain validation check to see if the domain is configured properly
    if domain_name is not None:
        click.echo(click.style("Validating domain name...", fg=CliColors.INFO.value))
        is_domain_valid = validate_domain(domain=domain_name)
        is_domain_validated = check_if_a_domain_is_validated(domain=domain_name)
        if not (is_domain_valid and is_domain_validated):
            click.echo(click.style("Error: Invalid domain name.", fg=CliColors.ERROR.value))
            return
    start_time = time.time() * 1000
    can_track = track_event(Events.DEPLOY_START.value, {"start_time": start_time})
    if not can_track:
        click.echo("You need to login to Tensorfuse to run your deployment.")
        click.echo("Please login using the command: " + click.style("tensorkube login", fg='cyan'))
        if config.get('github_actions'):
            raise Exception("Please provide the necessary credentials to deploy using tensorkube")
        return
    if config.get('gpus') not in [0, 1, 4, 8]:
        click.echo('Error: Invalid number of GPUs. Only supported values are 0, 1, 4, and 8.')
        return
    click.echo(click.style("Preparing image details", fg=CliColors.INFO.value))
    depl_secrets, env_namespace, image_tag, cwd, sanitised_project_name = create_deployment_details(secret=config.get('secret'),
                                                                                                  env=config.get('env'))
    if not image_tag:
        return
    enable_efs = False
    if config.get('efs'):
        enable_efs = True
    repo_url = get_or_create_ecr_repository(sanitised_project_name)
    image_url = f"{repo_url}:{image_tag}"
    
    convert_to_nydus_image = True  if config.get('gpus') > 0 and not enable_efs else False
    click.echo(click.style("Starting the build process...", fg=CliColors.INFO.value))
    pod_status = build_app(env=config.get('env'), image_tag=image_tag, sanitised_project_name=sanitised_project_name,
                           upload_to_nfs=enable_efs, image_url=image_url, convert_to_nydus_image=convert_to_nydus_image, secrets=config.get('secret'))
    if config.get('gpus') > 0:
        image_url = get_nydus_image_url(image_url=image_url)
    if enable_efs:
        image_url = image_tag
    deploy_knative_service(env=config.get('env'), gpus=config.get('gpus'),
                           gpu_type=config.get('gpu_type'), cpu=config.get('cpu'), memory=config.get('memory'),
                           min_scale=config.get('min_scale'), max_scale=config.get('max_scale'),concurrency= config.get('concurrency'), pod_status=pod_status,
                           cwd=cwd, sanitised_project_name=sanitised_project_name, image_url=image_url, secrets=depl_secrets,
                           enable_efs=enable_efs, domain=config.get('domain'),github_actions=config.get('github_actions'), readiness = config.get('readiness'), port = config.get('port'))

    end_time = time.time() * 1000
    track_event(Events.DEPLOY_END.value,
                {"start_time": start_time, "end_time": end_time, "duration": end_time - start_time})


# @tensorkube.command()
# def delete_project():
#     click.echo("Deleting the project resources...")
#     # TODO!: add logic to delete the ecr repository, s3 folder, build job, and any other resources
#     click.echo("Successfully deleted the project resources.")


@tensorkube.command()
def get_permissions_command():
    """Get the admin command needed to grant access to the current user.

    <Note>
    This command is only needed if you are not the initial user who created the EKS cluster.
    The user that doesn't have permissions needs to run this command and then send the resulting command
    to the admin user that provisioned the Tensorfuse runtime.
    </Note>
    """
    # TODO: give details of cluster user as well
    click.echo(f"Ask the initial user to run this command to grant you the necessary"
               f" permissions to the {get_cluster_name()} EKS cluster:")

    user_arn = get_aws_user_arn()
    if 'assumed-role' in user_arn:
        final_arn = sanitise_assumed_role_arn(user_arn)
    else:
        final_arn = user_arn

    click.echo("""\
    eksctl create iamidentitymapping \\
    --cluster {} \\
    --region {} \\
    --arn {} \\
    --group system:masters \\
    --username <USERNAME_OF_YOUR_CHOICE>""".format(get_cluster_name(), REGION, final_arn))

    click.echo("Once you have access to the cluster, run the following command to sync the config files:")
    click.echo("tensorkube sync")


@tensorkube.command()
def sync():
    """Sync the Tensorfuse configuration on a new machine.
    """
    click.echo("Syncing config files for the tensorkube cluster...")
    click.echo("Updating kubeconfig...")
    update_eks_kubeconfig()
    click.echo("Successfully updated the kubeconfig file.")


@tensorkube.group()
def deployment():
    """Manage and interact with your deployments."""
    pass


@deployment.command()
@click.option('--env', default=None, type=str, help='Environment to list the services from.')
@click.option('--all', is_flag=True, help='List all services from all environments.')
@click.option('--old', is_flag=True, help='List older sslip urls for using as hosts if you are on an older version.')
def list(env, all, old):
    """List all deployments running and recently stopped along with their status"""
    list_tensorkube_deployments(env_name=env, all=all, old=old)


@deployment.command()
@click.argument('service_name')
@click.option('--env', default=None, type=str, help='Environment to describe the deployment from.')
def describe(service_name, env):
    """List details of a deployment including the status, url and the latest ready revision."""
    describe_deployment(service_name=service_name, env_name=env)

@deployment.command()
@click.argument('service_name')
@click.option('--env', default=None, type=str, help='Environment to describe the deployment from.')
def delete(service_name, env):
    """Delete a deployment.

    <Warning>
    This action is destructive. Once a deployment is deleted it cannot be recovered.
    </Warning>
    """
    env_namespace = env if env else DEFAULT_NAMESPACE
    delete_deployment(service_name=service_name, env_name=env_namespace)


@deployment.command()
@click.argument('service_name')
@click.option('--env', default=None, type=str, help='Environment to list the services from.')
def logs(service_name, env):
    """Stream logs for a specific deployment if it is in the running state.

    Examples:
        Get the logs using the deployment name.

        ```bash
        tensorkube deployment logs demo-gpus-1-v100
        ```
    """
    env_namespace = env if env else DEFAULT_NAMESPACE
    display_deployment_logs(service_name=service_name, namespace=env_namespace)


@deployment.command()
@click.argument('service_name')
@click.option('--env', default=None, type=str, help='Environment to list the services from.')
def ssh(service_name, env):
    """SSH into the instances of a specific deployment.

    If multiple instances are running, this command gives you a list of instances to choose from.

    Examples:
        SSH into the deployment instance using deployment name.

        ```bash
        tensorkube deployment ssh demo-gpus-1-v100
        ```
    """
    click.echo("SSH into the deployment...")
    env_namespace = env if env else DEFAULT_NAMESPACE
    ssh_into_deployed_service(service_name=service_name, namespace=env_namespace)


# all environment specific commands
@tensorkube.group()
def environment():
    """
    Environments are subdivisions within workspaces that enable you to deploy the same application across different namespaces.
    Each environment operates independently, with its own set of Secrets. By default, any lookups performed by an application within
    a specific environment are scoped to entities in that same environment.

    A common use case for environments is to separate development and production workflows. This ensures that new features can be
    developed and tested in a dedicated development environment without risking changes to live production applications. At the same time,
    it allows seamless deployment of updates to the production environment when ready.

    <Note>
    Containers from different environments can run on the same nodes. However, they are isolated from each other.
    Apps in different environments still eat up your quotas. So, make sure to not keep the instances always running in your
    staging environments.
    </Note>
    """
    pass


@environment.command()
@click.option('--env-name', help='Name of the environment to create.')
def create(env_name):
    """Create a new environment.

    This also provisions the surrounding infrastructure needed for environments such as service accounts, IAM roles, registries and buckets.
    """
    click.echo("Creating a new environment...")
    create_new_environment(env_name=env_name)


@environment.command()
@click.option('--env-name', help='Name of the environment to delete.')
def delete(env_name):
    """Delete an environment.

    This command deletes all the deployed jobs and deployments in the environment.

    This also de-provisions all the surrounding infrastructure needed for environments such as service accounts, IAM roles, registries and buckets.

    <Warning>
    Please be careful while deleting an environment. This action is irreversible. All the jobs, queues and deployed applications in the environment will be deleted.
    </Warning>
    """
    click.echo("Deleting the environment...")
    delete_environment(env_name=env_name)


@environment.command()
def list():
    """List all the environments.
    """
    environments = list_environments()
    for env in environments:
        click.echo(env)


@tensorkube.command()
def login():
    """Log into Tensorfuse and obtain the usage token.

    Tensorfuse CLI requires obtaining a usage token from Tensorfuse.
    """
    click.echo("Opening the Tensorfuse dashboard in your default browser...")
    base_url = get_base_login_url()
    click.launch(base_url + "/tensorfuse/login?tensorkube_login=True")
    run_server()
    track_event(Events.LOGGED_IN.value, {})



@secret.command()
@click.option('--env', default=DEFAULT_NAMESPACE, type=str, help='Environment to create the secret in.')
@click.option('--force', is_flag=True, help='Update the secret if one with the same name already exists.')
@click.argument('secret_name', type=str)
@click.argument('key_value_pairs', nargs=-1)
def create(secret_name, key_value_pairs, env, force):
    """Create a new secret in the specified environment. Use `--force` to overwrite an existing one.
    """
    try:
        key_values = dict(pair.split('=',1) for pair in key_value_pairs)
    except Exception as e:
        click.echo(
            click.style("Error: Invalid key-value pairs. Please provide key-value pairs in the format KEY=value.",
                        fg=CliColors.ERROR.value))
        return

    click.echo("Creating secret " + click.style(secret_name, bold=True) + " in environment " + click.style(env,
                                                                                                           bold=True) + " ...")

    create_secret(name=secret_name, data=key_values, namespace=env, force=force)


@secret.command()
@click.option('--env', default=DEFAULT_NAMESPACE, type=str, help='Environment to delete the secret from.')
@click.argument('secret_name', type=str)
def delete(secret_name, env):
    """Delete a secret from the specified environment.

    <Warning>
    This action cannot be undone. Deleting a secret will affect all the deployments that are using that particular secret.
    They might completely fail to initialise. Use this command with caution.
    </Warning>
    """
    msg = "Are you sure you want to delete the secret? This action cannot be undone"
    if click.confirm(click.style(msg, fg=CliColors.WARNING.value), abort=True):
        click.echo("Deleting secret " + click.style(secret_name, bold=True) + " from environment " + click.style(env,
                                                                                                                 bold=True) + " ...")

        delete_secret(name=secret_name, namespace=env)


@secret.command()
@click.option('--env', default=DEFAULT_NAMESPACE, type=str, help='Environment to list the secrets from.')
def list(env):
    """List all the secrets in the specified environment.
    """
    secrets = list_secrets(env)
    if not secrets:
        if env == DEFAULT_NAMESPACE:
            click.echo("No secrets found")
        else:
            click.echo(f"No secrets found in environment " + click.style(env, bold=True))
        return
    display_secrets(secrets, env)


@tensorkube.command()
def test():
    click.echo("Running tests... for someone")
    


@tensorkube.command()
@click.option('--cloud', default='aws', help='Cloud provider to use.')
def reset(cloud):
    reset_cloud(cloud)


@tensorkube.group()
@click.option('--cloud', default='aws', help='Cloud provider to use.')
@click.pass_context
def dev(ctx, cloud):
    """Manage hot reloading development containers for the current user.
    """
    ctx.ensure_object(dict)
    ctx.obj['cloud'] = cloud
    time_now_utc = datetime.now(timezone.utc).isoformat()
    subcommand = ctx.invoked_subcommand
    if subcommand == "start":
        event = Events.DEVCONTAINER_START
    elif subcommand == "stop":
        event = Events.DEVCONTAINER_STOP
    elif subcommand == "delete":
        event = Events.DEVCONTAINER_DELETE
    elif subcommand == "list":
        event = Events.DEVCONTAINER_LIST
    else:
        event = Events.DEVCONTAINER
    can_track = track_event(event.value, {"start_time": time_now_utc})
    if not can_track:
        click.echo("You need to login to Tensorfuse to run your devcontainers.")
        click.echo("Please login using the command: " + click.style("tensorkube login", fg='cyan'))
        exit(0)


@dev.command()
@click.pass_context
def list(ctx):
    """List all the running / stopped devcontainers from the current user.
    """
    cloud = ctx.obj['cloud']
    list_instances_in_cloud(cloud)


@dev.command()
@click.option('--gpu-type',
              type=click.Choice(['V100', 'A10G', 'T4', 'L4', 'A100', 'L40S', 'H100', 'None'], case_sensitive=False),
              help='Type of GPU.')
@click.option('--port', type=int, default=8080, help='Port to run the devcontainer on.')
@click.pass_context
def start(ctx, gpu_type: str, port: int):
    """Spin up a new devcontainer from the current folder.

    The folder should contain a `Dockerfile`.
    """
    cloud = ctx.obj['cloud']
    if gpu_type == 'None':
        gpu_type = None
    start_devcontainer(cloud, gpu_type, port)


@dev.command()
@click.pass_context
def stop(ctx):
    """Stop a running development container.

    This is only available when the underlying cloud supports stopped instances. An advantage of stopping against deleting
    a devcontainer is that the SSD snapshot is cached and hence, the devcontainer can be started faster.

    However this incurs cost for the SSD snapshot.
    """
    cloud = ctx.obj['cloud']
    pause_devcontainer(cloud)


@dev.command()
@click.pass_context
def delete(ctx):
    """Purge a running / stopped development container.

    This command deletes all the associated resources of the development container including the attached block storage.
    """
    cloud = ctx.obj['cloud']
    purge_devcontainer(cloud)


@tensorkube.group()
def train():
    pass


@train.command()
@click.option('--gpus', default=DEFAULT_GPUS, help='Number of GPUs needed for the service.')
@click.option('--gpu-type', type=click.Choice(['V100', 'A10G', 'T4', 'L4', 'L40S', 'A100', 'H100'], case_sensitive=False),
              help='Type of GPU.')
@click.option('--env', default=DEFAULT_ENV, type=str, help='Environment to deploy the service to.')
@click.option('--job-id', default=None, type=str, help='Unique job id for the training job.')
@click.option('--axolotl', is_flag=True, help='Run the axolotl training job.')
@click.option('--config-path', default=None, type=str, help='Path to the config.yaml file.')
@click.option('--secret', default=DEFAULT_SECRET, type=str, multiple=True, help='Secret to use for the deployment.')
def create(gpus, gpu_type, env, job_id, axolotl, config_path, secret):
    if axolotl:
        axolotl_train(env=env, secrets=secret, gpus=gpus, gpu_type=gpu_type, job_id=job_id, config_path=config_path)
    else:
        click.echo("Invalid command. Please use the --axolotl flag to run the axolotl training job.")
        return


@train.command()
@click.option('--name', required=True, type=str, help='Name of the user to create.')
def create_user(name: str):
    click.echo("Creating a new user...")
    create_iam_user(name)
    policy_arn = create_eks_access_policy(f'{get_cluster_name()}-{name}-eks-access-policy')['Policy']['Arn']
    attach_policy_to_user(policy_arn, name)
    sqs_policy_arn = create_user_sqs_access_policy(f'{get_cluster_name()}-{name}-sqs-access-policy')['Policy']['Arn']
    attach_policy_to_user(sqs_policy_arn, name)
    s3_policy_arn = create_user_s3_access_policy(f'{get_cluster_name()}-{name}-s3-access-policy')['Policy']['Arn']
    attach_policy_to_user(s3_policy_arn, name)
    dynamo_policy_arn = create_user_dynamo_access_policy(f'{get_cluster_name()}-{name}-dynamo-access-policy')['Policy'][
        'Arn']
    attach_policy_to_user(dynamo_policy_arn, name)
    add_user_to_k8s(name)
    access_key, secret_access_key = create_access_key(name)
    prettify_aws_user_keys(access_key, secret_access_key)
    return


@train.command()
@click.option('--job-id', required=True, type=str, help='Unique job id for the training job.')
@click.option('--env', default=DEFAULT_ENV, type=str, help='Environment to deploy the service to.')
def logs(job_id: str, env: str):
    click.echo("Fetching logs for the training job...")
    job_prefix = get_job_prefix_from_job_id(job_id)
    namespace = env if env else DEFAULT_NAMESPACE
    display_job_logs(job_prefix=job_prefix, namespace=namespace)


@train.command()
@click.option('--env', default=DEFAULT_ENV, type=str, help='Environment to delete the job from.')
@click.option('--job-id', required=True, type=str, help='Unique job id for the training job.')
def delete(job_id: str, env: str):
    click.echo("Deleting the training job...")
    job_prefix = get_job_prefix_from_job_id(job_id)
    namespace = env if env else DEFAULT_NAMESPACE
    delete_tensorkube_job_by_prefix(job_prefix=job_prefix, namespace=namespace)


@train.command()
@click.option('--env', default=DEFAULT_ENV, type=str, help='Environment to deploy the service to.')
def list(env: str):
    namespace = env if env else DEFAULT_NAMESPACE
    # ax- for axolotl jobs
    prefix = 'ax-'
    list_tensorkube_training_jobs(namespace=namespace, job_prefix=prefix)


@train.command()
@click.option('--job-id', required=True, type=str, help='Unique job id for the training job.')
@click.option('--env', default=DEFAULT_ENV, type=str, help='Environment to deploy the service to.')
def get(job_id: str, env: str):
    namespace = env if env else DEFAULT_NAMESPACE
    # ax- for axolotl jobs
    job_prefix = get_job_prefix_from_job_id(job_id)
    get_tensorkube_training_job(job_prefix=job_prefix, namespace=namespace)


@tensorkube.group()
def datasets():
    """Manage datasets for Tensorkube
    """
    pass


@datasets.command()
def list():
    """List all the datasets created using Tensorkube cli.
    """
    list_tensorkube_datasets()


@datasets.command()
@click.option("--dataset-id", required=True, type=str, help="ID of the dataset to create.")
@click.option("--path", required=True,
              type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=str, readable=True),
              callback=lambda ctx, param, value: value if value.endswith('.jsonl') else click.BadParameter(
                  'File must be a .jsonl file'), help="Path to the JSONL file.")
def create(dataset_id, path):
    """Create a dataset using Tensorkube. This command creates a cloud bucket and stores your dataset in that bucket.
    """
    click.echo("Creating dataset...")
    upload_tensorkube_dataset(dataset_id=dataset_id, file_path=path)


@datasets.command()
@click.option("--dataset-id", required=True, type=str, help="ID of the dataset to delete.")
def delete(dataset_id: str):
    """Delete a dataset using Tensorkube cli.
    """
    delete_tensorkube_dataset(dataset_id=dataset_id)


@tensorkube.group()
def job():
    """Manage, deploy and queue jobs on Tensorfuse.
    """
    pass


@job.command()
@click.option('--name', required=True, type=str, help='Name of the job to deploy.')
@click.option('--gpus', default=DEFAULT_GPUS, help='Number of GPUs needed for an instance of the job.')
@click.option('--gpu-type', type=click.Choice(['V100', 'A10G', 'T4', 'L4', 'L40S', 'A100', 'H100'], case_sensitive=False),
              help='Type of GPU.')
@click.option('--cpu', type=float, default=DEFAULT_CPU, help='Number of CPU millicores. 1000 = 1 CPU')
@click.option('--memory', type=float, default=DEFAULT_MEMORY, help='Amount of RAM in megabytes.')
@click.option('--secret', default=DEFAULT_SECRET, type=str, multiple=True, help='Secrets that are required by the job.')
@click.option('--max-scale', type=int, default=DEFAULT_MAX_SCALE, help='Maximum number of jobs to run concurrently.')
@click.option('--update', is_flag=True, help='Update the job if it already exists.')
@click.option("--efs", is_flag = True, help="Flag to use EFS for the deployment.")
def deploy(name, gpus, gpu_type, cpu, memory, secret, max_scale, update, efs):
    """Deploy and orchestrate a job on Tenosrfuse.

    This command orchestrates the infrastructure needed for jobs such as queues, buckets and key-value stores.
    It also builds the container image for the job and pushes it to the container registry.
    """
    env = 'keda'
    start_time = time.time() * 1000
    can_track = track_event(Events.JOB_DEPLOY_START.value, {"start_time": start_time})
    if not can_track:
        click.echo("You need to login to Tensorfuse to run your deployment.")
        click.echo("Please login using the command: " + click.style("tensorkube login", fg='cyan'))
        return
    if gpus not in [0, 1, 4, 8]:
        click.echo('Error: Invalid number of GPUs. Only supported values are 0, 1, 4, and 8.')
        return

    # TODO: Check if job already exists and update it if the update flag is set
    does_job_exist, existing_job = is_existing_queued_job(name)
    if does_job_exist and not update:
        click.echo(
            f"Job with name {name} already exists. Please use a different name or use the --update flag to update the job.")
        return

    depl_secrets, env_namespace, image_tag, cwd, sanitised_project_name = create_deployment_details(secret=secret,
                                                                                                    env=env)

    if not cwd and not image_tag:
        return

    sanitised_job_name = sanitise_name(name)
    repo_url = get_or_create_ecr_repository(sanitised_project_name)
    image_url = f"{repo_url}:{image_tag}"
    convert_to_nydus_image = True if gpus > 0 and not efs else False
    pod_status = build_app(env=env, image_tag=image_tag, sanitised_project_name=sanitised_job_name, upload_to_nfs=efs,image_url=image_url, convert_to_nydus_image=convert_to_nydus_image, secrets=secret)
    if gpus > 0:
        image_url = get_nydus_image_url(image_url=image_url)
    if efs:
        image_url = image_tag
    if pod_status == 'Succeeded' or pod_status == 'Completed':
        deploy_job(env=env, job_name=name, gpus=gpus, gpu_type=gpu_type, cpu=cpu, memory=memory, max_scale=max_scale,
                   sanitised_project_name=sanitised_job_name, image_tag=image_url, secrets=depl_secrets, cwd=cwd, update=update, enable_efs=efs)
    else:
        click.echo("Failed to build the Docker image. Please check the logs for more details. Pod status: {}".format(
            pod_status))

    end_time = time.time() * 1000
    track_event(Events.JOB_DEPLOY_END.value,
                {"start_time": start_time, "end_time": end_time, "duration": end_time - start_time})


@job.command()
@click.option("--job-name", required=True, type=str, help="Name of the job to delete.")
def delete(job_name: str):
    """Delete a job from Tensorfuse.

    This command also de-provisions a job's infrastructure such as queues, buckets and key-value stores.
    """
    delete_all_job_resources(job_name)
    click.echo("Job deleted successfully.")


@job.command()
@click.option("--job-name", required=True, type=str, help="Name of the job to delete.")
@click.option("--job-id", required=True, type=str, help="Unique id for the job instance.")
@click.option("--payload", required=True, type=str, help="Payload of the job to delete.")
def queue(job_name: str, job_id: str, payload: str):
    """Queue an instance of a deployed job on Tensorfuse.

    The payload is a JSON string that is passed to the job instance.
    """
    queue_job(job_name, job_id, payload)
    click.echo("Job queued successfully.")


@job.command()
@click.option("--job-name", required=True, type=str, help="Name of the job to deploy.")
@click.option("--job-id", required=True, type=str, help="Unique id of the job instance.")
def get(job_name: str, job_id: str):
    """Get the status of a job instance.
    """
    status = get_job_status(job_name, job_id)
    print(status)


@job.command()
@click.option("--job-name", default=None, type=str, help="Name of the job to deploy.")
def list(job_name):
    """List all jobs or a specific job on Tensorfuse.

    1. If no job name is provided, all jobs are listed.
    2. If a job name is provided, the status of that job is displayed.
    """
    if not job_name:
        # Display for all jobs
        scaled_jobs = list_keda_scaled_jobs()
        queued_job_statuses = get_all_job_statuses()
        display_queued_jobs(scaled_jobs, queued_job_statuses)
    else:
        # Display for a specific job
        does_job_exist, existing_job = is_existing_queued_job(job_name)
        if not does_job_exist:
            click.echo(f"No job found with name: {job_name}")
            return
        else:
            dynamodb_job_statuses = get_job_statuses(job_name)
            display_specific_queued_job(existing_job, dynamodb_job_statuses)


@job.command()
@click.option("--job-name", required=True, type=str, help="Name of the job whose logs to display.")
def logs(job_name):
    """Stream the logs for a specific job instance.

    This command works only if the job is currently in progress.
    """
    display_job_logs(job_prefix=job_name, namespace='keda', container_name="sqs-job-1")


@tensorkube.group()
def domain():
    """Manage custom domain names and TLS for your Tensorkube cluster.
    """
    pass


@domain.command()
@click.option('--domain-name', required=True, help='Domain name for wildcard certificate')
def configure(domain_name):
    """Configure a wildcard subdomain for your Tensorkube platform.

    This command creates an ACM certificate for your wildcard domain and sets up DNS validation.

    Example:
        To assign your tensorfuse deployments a domain of the form `tfservice.sub.example.org` run the following command
        ```bash
        tensorkube domain configure --domain-name docdemo.tensorfuse.io
        ```
        This will configure a wildcard certificate for all the domains of the form `*.docdemo.tensorfuse.io`

    """
    deployed = configure_certificate(domain_name)
    if not deployed:
        return
    stack_name = get_certificate_stack_name(domain_name)
    validation_records = get_validation_records_with_wait(stack_name=stack_name)
    if validation_records is None:
        click.echo(click.style(f"Failed to retrieve validation records for domain: {domain_name}. "
                               f"Please configure the record using `tensorkube domain configure` or try again (race condition).",
                               fg='red'))
        return
    else:
        display_dns_records_table(domain_name, validation_records)


@domain.command()
@click.option('--domain-name', required=True, help='Domain name for wildcard certificate')
def attach(domain_name):
    """Associate the configured domain to your tensorfuse runtime post DNS validation.
    """
    attach_domain_name(domain_name)  # in the end configure 443 port for the ingress gateway


@domain.command()
@click.option('--domain-name', required=True, help='Domain name for wildcard certificate')
def get_validation_records(domain_name):
    """Get the DNS validation records and DNS routing records for the domain.
    """
    stack_name = get_certificate_stack_name(domain_name)
    validation_records = get_validation_records_from_events(stack_name=stack_name)
    if validation_records is None:
        click.echo(click.style(f"Failed to retrieve validation records for domain: {domain_name}. "
                               f"Please configure the record using `tensorkube domain configure`", fg='red'))
        return
    else:
        display_dns_records_table(domain_name, validation_records)


@tensorkube.command()
@click.option('--principal-arn', required=True, type=str, help='Principal ARN to give access to the cluster.')
def give_cluster_access(principal_arn: str):
    """Grant access to the EKS cluster to a user or role.
    """
    give_eks_cluster_access(principal_arn)


@tensorkube.command()
def get_principal_arn():
    """Display the principal ARN of the current AWS user. Useful when granting access to the cluster.
    """
    click.echo("Your principal ARN is: " + get_aws_user_principal_arn())


@tensorkube.command()
def version():
    print_tensorkube_version()