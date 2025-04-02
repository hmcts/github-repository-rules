# GitHub Repository Rules

This repository contains code to manage GitHub repository branch protection rules for HMCTS.

# Overview

This Terraform configuration automates the process of setting up rule sets at the organisation level.

- [Rate Limits Page](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api?apiVersion=2022-11-28)

<!--START_PRODUCTION_COUNT-->

| **Repository Type**       | **Count** |
|---------------------------|-----------|
| Production Repositories   | [317](../production-repos.json)        |
| Development Repositories  | 0        |
<!--END_PRODUCTION_COUNT-->

## Getting Started

### Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) (version 1.5.7 or later)
- Oauth or PAT Token with appropriate permissions.


## What This Does

- Reads a list of repositories from `production-repos.json`
- Creates a ruleset at the organisation level, this applies standardisation across all repositories.
- Creates custom properties for repositories, such as marking repositories as "is_production."
- A good note to make is that you do not have to update this codebase as it will pull any new production repositories from the URL's provided and update itself at midnight.
- If you want to you can add repositories in yourself by raising a PR from main, add your repositories to the production-repos.json. Then merge the PR once ready.


## Maintenance

To add or remove repositories follow the below:

1. Open a fresh PR from the master branch ensuring you have pulled down recent changes to the master branch.
2. Applies standardised rule sets to repositories listed in the `production-repos.json` file, ensuring consistent management and configuration across all repositories.
3. Create a PR and allow the GH Actions pipeline to run a Terraform Plan to confirm changes are accepted.
4. Once the plan is good, you can merge your PR into main branch and the pipeline will trigger an apply.
5. Once applied delete your branch.


## Troubleshooting

- Check your Terraform version and ensure there are no underlying bugs with the provider versions.
- Ensure you have formatted your repository name correctly as it may not pick it up properly.

## Terraform documentation

## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.5.7 |
| <a name="requirement_github"></a> [github](#requirement\_github) | ~> 6.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_azurerm"></a> [azurerm](#provider\_azurerm) | n/a |
| <a name="provider_github"></a> [github](#provider\_github) | ~> 6.0 |
| <a name="provider_local"></a> [local](#provider\_local) | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_tags"></a> [tags](#module\_tags) | git::https://github.com/hmcts/terraform-module-common-tags.git | master |

## Resources

| Name | Type |
|------|------|
| [azurerm_resource_group.rg](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/resource_group) | resource |
| [azurerm_storage_account.sa](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_account) | resource |
| [azurerm_storage_container.tfstate](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_container) | resource |
| [github_organization_ruleset.default_ruleset](https://registry.terraform.io/providers/integrations/github/latest/docs/resources/organization_ruleset) | resource |
| [github_team.admin](https://registry.terraform.io/providers/integrations/github/latest/docs/data-sources/team) | data source |
| [local_file.repos_json](https://registry.terraform.io/providers/hashicorp/local/latest/docs/data-sources/file) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_builtFrom"></a> [builtFrom](#input\_builtFrom) | Information about the build source or version | `string` | `"https://github.com/hmcts/github-repository-rules"` | no |
| <a name="input_env"></a> [env](#input\_env) | The environment for the deployment (e.g., dev, staging, prod) | `string` | `"dev"` | no |
| <a name="input_location"></a> [location](#input\_location) | The location for the resources | `string` | `"UK South"` | no |
| <a name="input_oauth_token"></a> [oauth\_token](#input\_oauth\_token) | OAUTH token to use for authentication. | `string` | n/a | yes |
| <a name="input_override_action"></a> [override\_action](#input\_override\_action) | The action to override | `string` | `"plan"` | no |
| <a name="input_product"></a> [product](#input\_product) | The product name or identifier | `string` | `"sds-platform"` | no |
| <a name="input_resource_group_name"></a> [resource\_group\_name](#input\_resource\_group\_name) | The name of the resource group | `string` | `"rule-set-rg"` | no |
| <a name="input_storage_account_name"></a> [storage\_account\_name](#input\_storage\_account\_name) | The name of the storage account | `string` | `"rulesetsa"` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_common_tags"></a> [common\_tags](#output\_common\_tags) | n/a |
