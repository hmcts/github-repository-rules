provider "github" {
  token = var.github_token
  owner = "hmcts"
}

terraform {
  required_version = ">= 1.3.6"

  #   backend "azurerm" {
  #   }
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.109.0"
    }
  }
}

provider "azurerm" {
  features {}
}