pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS_ID = 'dockerhub'
        DOCKER_HUB_REPO = 'isurukavinda99/order_api'
        K8S_DEPLOY_FILE = 'order-deployment.yaml'
        K8S_SERVICE_FILE = 'order-service.yaml'

        // Your environment variables for testing & deployment
        DB_HOST = 'iit-cc-assignment.cg7k80goqzon.us-east-1.rds.amazonaws.com'
        DB_NAME = 'test_iit_game_service'
        DB_USER = 'root'
        DB_PASSWORD = 'iitCCAsign1'
        DB_PORT = '3306'
        COGNITO_USER_POOL_ID = 'us-east-1_SGSijIBP0'
        COGNITO_CLIENT_ID = '79kvjkpkt94sksjel3f0720834'
        AWS_REGION = 'us-east-1'
        // Note: Put sensitive tokens in Jenkins credentials, not here in plain text
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo '=== Building Docker Image ==='
                    dockerImage = docker.build("${DOCKER_HUB_REPO}:latest")
                }
            }
        }

        stage('Run API Tests') {
            steps {
                script {
                    echo '=== Running Tests in Docker Container ==='
                    sh """
                        docker run --rm \\
                            -e DB_HOST=${DB_HOST} \\
                            -e DB_NAME=${DB_NAME} \\
                            -e DB_USER=${DB_USER} \\
                            -e DB_PASSWORD=${DB_PASSWORD} \\
                            -e DB_PORT=${DB_PORT} \\
                            -e COGNITO_USER_POOL_ID=${COGNITO_USER_POOL_ID} \\
                            -e COGNITO_CLIENT_ID=${COGNITO_CLIENT_ID} \\
                            -e AWS_REGION=${AWS_REGION} \\
                            ${DOCKER_HUB_REPO}:latest pytest app/tests/integration || exit 1
                    """
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', "${DOCKER_HUB_CREDENTIALS_ID}") {
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Install kubectl') {
            steps {
                sh '''
                    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                    chmod +x kubectl
                    mkdir -p $HOME/bin
                    mv kubectl $HOME/bin/kubectl
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh """
                        export PATH=$HOME/bin:$PATH
                        kubectl apply -f ${K8S_DEPLOY_FILE} --validate=false
                        kubectl apply -f ${K8S_SERVICE_FILE} --validate=false
                        kubectl rollout restart deployment/order-api-deployment
                        kubectl rollout status deployment/order-api-deployment
                    """
                }
            }
        }
    }

    post {
        success {
            echo '✅ Order API deployed successfully!'
        }
        failure {
            echo '❌ Deployment failed. Please check logs.'
        }
    }
}
