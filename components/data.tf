data "github_organization" "org" {
  name = "hmcts-test"
}

data "local_file" "repos_json" {
  filename = "${path.module}./production-repos.json"
}

# Fetch existing branches for each repository
data "github_branch" "existing_branches" {
  for_each = {
    for combo in local.repo_branch_combinations : "${combo.repo}:${combo.branch}" => combo
  }

  repository = each.value.repo
  branch     = each.value.branch
}

data "github_repository_rulesets" "existing" {
  for_each   = toset(local.included_repositories)
  repository = each.value
}