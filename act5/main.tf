terraform {
    required_providers {
      docker = {
        source = "kreuzwerker/docker"
        version = "~> 3.0.2"
      }
    }
}

provider "docker" {}
resource "docker_image" "todo-service" {
    name="phoeng/todo:3.0"
    keep_locally=false
}

  
resource "docker_image" "redis" {
  name="redis"
  keep_locally=false
}

resource "docker_image" "todo-noti" {
  name="phoeng/todo-notification:1.1"
  keep_locally = false
}

resource "docker_network" "todo_net" {
  name = "todo_netwowrk"
}

resource "docker_container" "todo-service" {
  image=docker_image.todo-service.image_id
  name="todo-service"
  ports{
    internal=8000
    external=8000
  }
  env = [
    "REDIS_HOST=redis",
    "REDIS_PORT=6379",
    "NOTIFICATION_HOST=notification"
  ]
  networks_advanced {
    name = docker_network.todo_net.name
  }
}

resource "docker_container" "redis" {
    image=docker_image.redis.image_id
    name="redis"
    ports{
        internal=6379
        external=6379
    }
    networks_advanced {
      name = docker_network.todo_net.name
    }
}

resource "docker_container" "notification" {
  image = docker_image.todo-noti.image_id
  name = "notification"
  ports {
    internal = 9000
    external = 9000
  }
  networks_advanced {
    name = docker_network.todo_net.name
  }
}

output "todo_id" {
  value = docker_container.todo-service.id
}

output "todo_addr" {
  value = docker_container.todo-service.network_data[0].ip_address
}

output "redis_id" {
  value = docker_container.redis.id
}

output "redis_addr" {
  value = docker_container.redis.network_data[0].ip_address
}

output "noti_id" {
  value = docker_container.notification.id
}

output "noti_addr" {
  value = docker_container.notification.network_data[0].ip_address
}