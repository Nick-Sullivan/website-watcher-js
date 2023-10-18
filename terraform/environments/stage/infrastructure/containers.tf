
resource "terraform_data" "preview_docker_build" {
  triggers_replace = [
    md5(file("${local.lambda_dir}/Dockerfile.preview")),
    data.archive_file.layer.output_base64sha256,
    data.archive_file.handler.output_base64sha256,
  ]
  provisioner "local-exec" {
    working_dir = local.lambda_dir
    command     = "aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin ${local.aws_account_id}.dkr.ecr.ap-southeast-2.amazonaws.com"
  }
  provisioner "local-exec" {
    command = "docker pull ${data.aws_ssm_parameter.ecr_url.value}:base"
  }
  provisioner "local-exec" {
    working_dir = local.lambda_dir
    command     = "docker build -t ${data.aws_ssm_parameter.ecr_url.value}:preview -f Dockerfile.preview --build-arg=BASE_IMAGE_NAME=${data.aws_ssm_parameter.ecr_url.value}:base ."
  }
}

resource "terraform_data" "preview_docker_push" {
  depends_on = [
    terraform_data.preview_docker_build,
  ]
  lifecycle {
    replace_triggered_by = [terraform_data.preview_docker_build]
  }
  provisioner "local-exec" {
    working_dir = local.lambda_dir
    command     = "aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin ${local.aws_account_id}.dkr.ecr.ap-southeast-2.amazonaws.com"
  }
  provisioner "local-exec" {
    working_dir = local.lambda_dir
    command     = "docker push ${data.aws_ssm_parameter.ecr_url.value}:preview"
  }
}

data "aws_ecr_image" "preview_docker_image" {
  depends_on = [
    terraform_data.preview_docker_push
  ]
  repository_name = data.aws_ssm_parameter.ecr_name.value
  image_tag       = "preview"
}

resource "terraform_data" "scrape_docker_build" {
  triggers_replace = [
    md5(file("${local.lambda_dir}/Dockerfile.scrape_website")),
    data.archive_file.layer.output_base64sha256,
    data.archive_file.handler.output_base64sha256,
  ]
  provisioner "local-exec" {
    working_dir = local.lambda_dir
    command     = "aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin ${local.aws_account_id}.dkr.ecr.ap-southeast-2.amazonaws.com"
  }
  provisioner "local-exec" {
    command = "docker pull ${data.aws_ssm_parameter.ecr_url.value}:base"
  }
  provisioner "local-exec" {
    working_dir = local.lambda_dir
    command     = "docker build -t ${data.aws_ssm_parameter.ecr_url.value}:scrape -f Dockerfile.scrape_website --build-arg=BASE_IMAGE_NAME=${data.aws_ssm_parameter.ecr_url.value}:base ."
  }
}

resource "terraform_data" "scrape_docker_push" {
  depends_on = [
    terraform_data.scrape_docker_build,
  ]
  lifecycle {
    replace_triggered_by = [terraform_data.scrape_docker_build]
  }
  provisioner "local-exec" {
    working_dir = local.lambda_dir
    command     = "aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin ${local.aws_account_id}.dkr.ecr.ap-southeast-2.amazonaws.com"
  }
  provisioner "local-exec" {
    working_dir = local.lambda_dir
    command     = "docker push ${data.aws_ssm_parameter.ecr_url.value}:scrape"
  }
}

data "aws_ecr_image" "scrape_docker_image" {
  depends_on = [
    terraform_data.scrape_docker_push
  ]
  repository_name = data.aws_ssm_parameter.ecr_name.value
  image_tag       = "scrape"
}
