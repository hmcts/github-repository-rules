module "tags" {
  source      = "git::https://github.com/hmcts/terraform-module-common-tags.git?ref=master"
  environment = var.env
  product     = var.product
  builtFrom   = var.builtFrom
}

resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
  tags     = module.tags.common_tags
}

resource "azurerm_storage_account" "sa" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  tags                     = module.tags.common_tags
}

resource "azurerm_storage_container" "tfstate" {
  name                  = "tfstate"
  storage_account_name  = azurerm_storage_account.sa.name
  container_access_type = "private"
}

resource "github_organization_ruleset" "default_ruleset" {
  name        = "Default Branch Protection"
  target      = "branch"
  enforcement = "active"

  conditions {
    repository_name {
      include = local.included_repositories
      exclude = [] # You can add exceptions here if needed
    }
    ref_name {
      include = ["refs/heads/main", "refs/heads/master"]
      exclude = []
    }
  }

  rules {
    creation                = null
    update                  = null
    deletion                = false
    required_linear_history = true

    pull_request {
      dismiss_stale_reviews_on_push     = true
      require_code_owner_review         = false
      required_approving_review_count   = 1
      require_last_push_approval        = true
      required_review_thread_resolution = true
    }

    required_status_checks {
      strict_required_status_checks_policy = true
      required_check {
        context = "ci/lint"
      }
      required_check {
        context = "ci/test"
      }
    }
  }
}