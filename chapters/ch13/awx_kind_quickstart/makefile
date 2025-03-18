KIND_CLUSTER_NAME ?= awx-cluster-demo
KIND_CONFIG_FILE ?= kind-config.yaml
AWX_INSTANCE_FILE ?= awx.yaml
HELM_CHART_VERSION ?=

# Conditionally set the helm version flag if HELM_CHART_VERSION is non-empty
HELM_VERSION_FLAG = $(if $(HELM_CHART_VERSION),--version $(HELM_CHART_VERSION),)

.DEFAULT_GOAL := help

.PHONY: help build-kind-cluster delete-kind-cluster helm-repo-add helm-install-awx helm-list-versions helm-get-values awx-describe-crd awx-instance-apply awx-instance-delete awx-instance-password demo-build demo-delete

help: ## Display this help message.
	@echo "Available tasks:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-25s %s\n", $$1, $$2}'

kind-cluster-build: ## Create Kind cluster.
	@echo "Creating Kind cluster '$(KIND_CLUSTER_NAME)'..."
	kind create cluster --name $(KIND_CLUSTER_NAME) --config $(KIND_CONFIG_FILE)

kind-cluster-delete: ## Delete Kind cluster.
	@echo "Deleting Kind cluster '$(KIND_CLUSTER_NAME)'..."
	kind delete cluster --name $(KIND_CLUSTER_NAME)

helm-repo-add: ## Add helm repository for AWX Operator.
	@echo "Adding helm repository for AWX Operator..."
	helm repo add awx-operator https://ansible-community.github.io/awx-operator-helm/
	helm repo update

helm-install-awx: ## Install/upgrade AWX Operator.
	@echo "Installing/upgrading AWX Operator..."
	helm upgrade --install awx-operator awx-operator/awx-operator $(HELM_VERSION_FLAG) -n awx --create-namespace

helm-list-versions: ## List available AWX Operator chart versions.
	@echo "Listing available AWX Operator chart versions..."
	helm search repo awx-operator/awx-operator --versions

helm-get-values: ## Show AWX Operator chart default values.
	@echo "Displaying AWX Operator chart default values..."
	helm show values awx-operator/awx-operator

awx-describe-crd: ## Describe AWX CRD. ⚠️ Must have AWX Operator helm chart installed.
	kubectl describe crd awxs.awx.ansible.com


awx-instance-apply: ## Apply AWX instance manifest.
	kubectl apply -f $(AWX_INSTANCE_FILE) --namespace awx

awx-instance-delete: ## Delete AWX instance.
	kubectl delete -f $(AWX_INSTANCE_FILE) --namespace awx

awx-instance-password: ## Get AWX instance password.
	@echo "AWX username: admin"
	@echo "AWX password: $(shell kubectl get secret --namespace awx awx-admin-password -o jsonpath="{.data.password}" | base64 --decode)"

demo-build: ## Build demo environment.
	make kind-cluster-delete || true
	make kind-cluster-build
	make helm-repo-add
	make helm-install-awx
	make awx-instance-apply

demo-delete: ## Delete demo environment.
	make kind-cluster-delete