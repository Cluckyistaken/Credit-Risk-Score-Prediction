pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = 'cluckyistaken'
        IMAGE_TAG = "${BUILD_NUMBER}"
        KUBECONFIG = "C:\\Users\\dolit\\.kube\\config"
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
                    // Using bat for Windows compatibility
                    bat 'pip install -r requirements.txt'
                    bat 'python manage.py test'
                }
            }
        }

        stage('Build & Push') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        // Login to Docker Hub
                        bat 'docker login -u %DOCKER_USER% -p %DOCKER_PASS%'

                        // Build and Push Backend
                        bat "docker build -t ${DOCKER_HUB_USER}/credit-risk-backend:${IMAGE_TAG} ./backend"
                        bat "docker push ${DOCKER_HUB_USER}/credit-risk-backend:${IMAGE_TAG}"

                        // Build and Push Frontend
                        bat "docker build -t ${DOCKER_HUB_USER}/credit-risk-frontend:${IMAGE_TAG} ./frontend"
                        bat "docker push ${DOCKER_HUB_USER}/credit-risk-frontend:${IMAGE_TAG}"

                        // Build and Push ML Service
                        bat "docker build -t ${DOCKER_HUB_USER}/credit-risk-ml:${IMAGE_TAG} ./ml-service"
                        bat "docker push ${DOCKER_HUB_USER}/credit-risk-ml:${IMAGE_TAG}"

                        // Build and Push Nginx
                        bat "docker build -t ${DOCKER_HUB_USER}/credit-risk-nginx:${IMAGE_TAG} ./infra/nginx"
                        bat "docker push ${DOCKER_HUB_USER}/credit-risk-nginx:${IMAGE_TAG}"

                        // Build and Push Database
                        bat "docker build -t ${DOCKER_HUB_USER}/credit-risk-database:${IMAGE_TAG} ./database"
                        bat "docker push ${DOCKER_HUB_USER}/credit-risk-database:${IMAGE_TAG}"
                        
                        // Logout for security
                        bat 'docker logout'
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Replace %IMAGE_TAG% placeholder with actual build number using PowerShell
                    powershell """
                        (Get-Content k8s/services-k8s.yaml) -replace '%IMAGE_TAG%', '${IMAGE_TAG}' | Set-Content k8s/services-k8s.yaml
                        (Get-Content k8s/gateway-k8s.yaml) -replace '%IMAGE_TAG%', '${IMAGE_TAG}' | Set-Content k8s/gateway-k8s.yaml
                        (Get-Content k8s/infra-k8s.yaml) -replace '%IMAGE_TAG%', '${IMAGE_TAG}' | Set-Content k8s/infra-k8s.yaml
                    """

                    // Apply Kubernetes manifests
                    bat 'kubectl apply -f k8s/infra-k8s.yaml'
                    bat 'kubectl apply -f k8s/services-k8s.yaml'
                    bat 'kubectl apply -f k8s/gateway-k8s.yaml'

                    // Restart deployments to pick up new images
                    bat 'kubectl rollout restart deployment backend frontend ml-service nginx'
                }
            }
        }
    }
}
