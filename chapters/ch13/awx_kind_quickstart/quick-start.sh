#!/bin/bash
set -e

# Default values
DEFAULT_CLUSTER_NAME="awx-cluster-demo"
DEFAULT_HOST_PORT=8383

# Parse command-line options (-c for cluster name, -p for host port)
while getopts "c:p:" opt; do
  case ${opt} in
    c)
      CLUSTER_NAME="$OPTARG"
      ;;
    p)
      HOST_PORT="$OPTARG"
      ;;
    *)
      echo "Usage: $0 [-c cluster_name] [-p host_port]"
      exit 1
      ;;
  esac
done
shift $((OPTIND - 1))

# Set variables to default values if not provided
CLUSTER_NAME=${CLUSTER_NAME:-$DEFAULT_CLUSTER_NAME}
HOST_PORT=${HOST_PORT:-$DEFAULT_HOST_PORT}

echo "Using cluster name: $CLUSTER_NAME"
echo "Using host port: $HOST_PORT"

# Inline Kind cluster configuration with variable expansion
KIND_CONFIG=$(cat <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30000
    hostPort: ${HOST_PORT}
    protocol: TCP
EOF
)

# Inline AWX manifest configuration (AWX instance uses nodeport 30000)
AWX_MANIFEST=$(cat <<'EOF'
---
apiVersion: awx.ansible.com/v1beta1
kind: AWX
metadata:
  name: awx-demo
  namespace: awx
spec:
  service_type: nodeport
  nodeport_port: 30000
EOF
)

echo "Deleting existing Kind cluster '$CLUSTER_NAME' (if any)..."
kind delete cluster --name "$CLUSTER_NAME" || true

echo "Creating Kind cluster '$CLUSTER_NAME'..."
# Write the inline Kind configuration to a temporary file
tmp_kind=$(mktemp)
echo "$KIND_CONFIG" > "$tmp_kind"
kind create cluster --name "$CLUSTER_NAME" --config "$tmp_kind"
rm "$tmp_kind"

echo "Adding AWX Operator Helm repository..."
helm repo add awx-operator https://ansible-community.github.io/awx-operator-helm/ || true
helm repo update

echo "Installing/upgrading AWX Operator using Helm..."
helm upgrade --install awx-operator awx-operator/awx-operator -n awx --create-namespace

echo "Applying AWX instance manifest..."
# Write the inline AWX manifest to a temporary file
tmp_awx=$(mktemp)
echo "$AWX_MANIFEST" > "$tmp_awx"
kubectl apply -f "$tmp_awx" --namespace awx
rm "$tmp_awx"

echo "Demo build complete."



# Show the admin password
echo "Waiting for AWX admin password to be available..."
while ! kubectl get secret awx-demo-admin-password -n awx &> /dev/null; do
  sleep 1
done
echo "AWX username: admin"
echo "AWX password: $(kubectl get secret awx-demo-admin-password -n awx -o jsonpath='{.data.password}' | base64 --decode)"
