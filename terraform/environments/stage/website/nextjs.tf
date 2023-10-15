
# TODO - a better method to work out if we need to redeploy
data "archive_file" "website" {
  type        = "zip"
  source_dir  = local.website_dir
  output_path = "${path.root}/website.zip"
  excludes    = [".next", "out", "node_modules"]
}

resource "terraform_data" "build" {
  triggers_replace = [
    data.archive_file.website.output_base64sha256
  ]
  provisioner "local-exec" {
    working_dir = local.website_dir
    command     = "npm run build"
  }
}
