

resource "aws_ecr_repository" "lambda_base" {
  name                 = local.prefix_lower
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = false
  }
}

resource "aws_ecr_lifecycle_policy" "lambda_base" {
  repository = aws_ecr_repository.lambda_base.name

  # May take up to 24 hours to expire old images
  policy = <<EOF
    {
        "rules": [
        {
            "rulePriority": 1,
            "description": "Expire untagged images",
            "selection": {
                "tagStatus": "untagged",
                "countType": "imageCountMoreThan",
                "countNumber": 1
            },
            "action": {
            "type": "expire"
            }
        }
        ]
    }
    EOF
}

resource "terraform_data" "base_docker_build" {
  triggers_replace = [
    md5(file("${local.lambda_dir}/Dockerfile.base")),
  ]
  provisioner "local-exec" {
    working_dir = local.lambda_dir
    command     = "docker build -t ${aws_ecr_repository.lambda_base.repository_url}:base -f Dockerfile.base ."
  }
}

resource "terraform_data" "base_docker_push" {
  depends_on = [
    terraform_data.base_docker_build,
  ]
  lifecycle {
    replace_triggered_by = [terraform_data.base_docker_build]
  }
  provisioner "local-exec" {
    working_dir = local.lambda_dir
    command     = "aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin ${local.aws_account_id}.dkr.ecr.ap-southeast-2.amazonaws.com"
  }
  provisioner "local-exec" {
    working_dir = local.lambda_dir
    command     = "docker push ${aws_ecr_repository.lambda_base.repository_url}:base"
  }
}

data "aws_ecr_image" "base_docker_image" {
  depends_on = [
    terraform_data.base_docker_push
  ]
  repository_name = aws_ecr_repository.lambda_base.name
  image_tag       = "base"
}
