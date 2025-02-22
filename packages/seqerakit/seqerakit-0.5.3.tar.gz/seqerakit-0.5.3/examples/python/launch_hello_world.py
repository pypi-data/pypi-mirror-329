import logging

# Import the seqerakit package
from seqerakit import seqeraplatform

logging.basicConfig(level=logging.DEBUG)

# Construct a new seqerakit SeqeraPlatform instance
tw = seqeraplatform.SeqeraPlatform(json=True)

# Customise the entries below as required
workspace = "scidev/gcp"  # Name of your Workspace
compute_env = "tower_cloud_testing_finland_nofusionv2"  # Name of your Compute Environment

# Specify a human-readable run name
run_name = "hello-world-seqerakit"

# Launch the 'hello-world' pipeline using the 'launch' method
pipeline_run = tw.launch(
    "--workspace",
    workspace,
    "--compute-env",
    compute_env,
    "--name",
    run_name,
    "--revision",
    "master",
    "--wait",
    "SUBMITTED",
    "https://github.com/nextflow-io/hello",
)
