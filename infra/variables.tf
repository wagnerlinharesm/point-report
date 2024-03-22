variable "region" {
  type    = string
  default = "us-east-2"
}

variable "point_report_sqs_queue_name" {
  type    = string
  default = "point_report"
}

variable "point_db_host" {
  type    = string
  default = "rdsproxy.proxy-cqivfynnpqib.us-east-2.rds.amazonaws.com"
}

variable "point_db_database" {
  type    = string
  default = "pointdb"
}

variable "point_db_secretsmanager_secret_name" {
  type    = string
  default = "mikes/db/db_credentials"
}

variable "mail_sender" {
  type    = string
  default = "rm349538@fiap.com.br"
}

variable "smtp_host" {
  type    = string
  default = "email-smtp.us-east-2.amazonaws.com"
}

variable "smtp_port" {
  type    = number
  default = 587
}

variable "smtp_credentials_secretsmanager_secret_name" {
  type    = string
  default = "smtp"
}

variable "report_point_bucket_name" {
  type    = string
  default = "cached-point-report-bucket-644237782704"
}


