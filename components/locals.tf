locals {
  env_display_names = {
    sbox    = "Sandbox"
    prod    = "Production"
    nonprod = "Non-Production"
    test    = "Test"
    staging = "staging"
  }
  common_tags = {
    "managedBy"          = "DevOps"
    "solutionOwner"      = "RDO"
    "activityName"       = "Storage Account"
    "dataClassification" = "Internal"
    "automation"         = ""
    "costCentre"         = ""
  }
  enforced_tags = module.tags.common_tags
}