pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = 'docker-hub-credentials'
        DOCKER_HUB_USER = 'cluckyistaken'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend Tests') {
            steps {
                dir('backend') {
                    // Install dependencies and run tests
                    // Using PowerShell as the environment is Windows
                    powershell 'pip install -r requirements.txt'
                    powershell 'python manage.py test'
                }
            }
        }

        stage('Build & Push') {
            steps {
                script {
                    docker.withRegistry('', "${DOCKER_HUB_CREDENTIALS}") {
                        // Build and Push Backend
                        def backendImage = docker.build("${DOCKER_HUB_USER}/credit-risk-backend:${IMAGE_TAG}", "./backend")
                        backendImage.push()

                        // Build and Push Frontend
                        def frontendImage = docker.build("${DOCKER_HUB_USER}/credit-risk-frontend:${IMAGE_TAG}", "./frontend")
                        frontendImage.push()

                        // Build and Push ML Service
                        def mlImage = docker.build("${DOCKER_HUB_USER}/credit-risk-ml:${IMAGE_TAG}", "./ml-service")
                        mlImage.push()

                        // Build and Push Nginx
                        def nginxImage = docker.build("${DOCKER_HUB_USER}/credit-risk-nginx:${IMAGE_TAG}", "./infra/nginx")
                        nginxImage.push()
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Replace %IMAGE_TAG% placeholder with actual build number
                    powershell """
                        (Get-Content k8s/services-k8s.yaml) -replace '%IMAGE_TAG%', '${IMAGE_TAG}' | Set-Content k8s/services-k8s.yaml
                        (Get-Content k8s/gateway-k8s.yaml) -replace '%IMAGE_TAG%', '${IMAGE_TAG}' | Set-Content k8s/gateway-k8s.yaml
                    """

                    // Apply Kubernetes manifests
                    powershell 'kubectl apply -f k8s/infra-k8s.yaml'
                    powershell 'kubectl apply -f k8s/services-k8s.yaml'
                    powershell 'kubectl apply -f k8s/gateway-k8s.yaml'

                    // Restart deployments to pick up new images
                    powershell 'kubectl rollout restart deployment backend frontend ml-service nginx'
                }
            }
        }
    }
}
