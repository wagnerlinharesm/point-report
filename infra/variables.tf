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
