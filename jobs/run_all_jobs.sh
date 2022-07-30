pwd_orig=$(pwd)
parent_path_of_script=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

echo cd-ing into $parent_path_of_script
cd "$parent_path_of_script"

amlt run -y ./amlt.yaml --target-name V100-1x-ded :train_1_node_1_gpu ml-template-mnist;
amlt run -y ./amlt.yaml --target-name V100-4x-ded :train_1_node_4_gpus ml-template-mnist;
amlt run -y ./amlt.yaml --target-name V100-4x-ded :train_distributed_2_nodes_4_gpus ml-template-mnist;
amlt run -y ./amlt.yaml --target-name V100-4x-ded :train_distributed_2_nodes_4_gpus_env_vars ml-template-mnist

echo cd-ing back to $pwd_orig
cd "$pwd_orig"
