#!/bin/bash
set -e

# Default values
EDA_HOST_PORT=8384

# Parse command-line options (-c for cluster name, -p for host port)
while getopts "c:p:" opt; do
  case ${opt} in
    p)
      HOST_PORT="$OPTARG"
      ;;
    *)
      echo "Usage: $0 [-p host_port]"
      exit 1
      ;;
  esac
done
shift $((OPTIND - 1))

# Set variables to default values if not provided
# CLUSTER_NAME=${CLUSTER_NAME:-$DEFAULT_CLUSTER_NAME}
HOST_PORT=${HOST_PORT:-$EDA_HOST_PORT}
PUBLIC_IP=$(curl -s ifconfig.me)

# Inline EDA manifest configuration (EDA instance uses nodeport 30001)
EDA_MANIFEST=$(cat <<'EOF'
apiVersion: eda.ansible.com/v1alpha1
kind: EDA
metadata:
  name: eda-demo
  namespace: eda-server-operator-system
spec:
  service_type: nodeport
  nodeport_port: 30001
  automation_server_url: http://{$PUBLIC_IP}:${HOST_PORT}
  automation_server_ssl_verify: "no"
  admin_user: admin
  loadbalancer_port: 80
  loadbalancer_protocol: http
EOF
)

echo "Installing/upgrading EDA Server Operator using Kubectl..."
kubectl apply -f https://github.com/ansible/eda-server-operator/releases/download/1.0.0/operator.yaml

echo "Applying EDA instance manifest..."
# Write the inline AWX manifest to a temporary file
tmp_eda=$(mktemp)
echo "$EDA_MANIFEST" > "$tmp_eda"
kubectl apply -f "$tmp_eda" --namespace eda-server-operator-system
rm "$tmp_eda"

echo "Demo EDA build complete."

# Show the admin password
echo "Waiting for EDA admin password to be available..."
while ! kubectl get secret eda-demo-admin-password -n eda-server-operator-system &> /dev/null; do
  sleep 1
done
echo "EDA Server username: admin"
echo "EDA Server password: $(kubectl get secret eda-demo-admin-password -n eda-server-operator-system -o jsonpath='{.data.password}' | base64 --decode)"
echo "You can access the EDA Server at: http://$PUBLIC_IP:$HOST_PORT"
echo "Note: The EDA Server may take a few minutes to become fully operational."
