pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS_ID = 'dockerhub'
        DOCKER_HUB_REPO = 'isurukavinda99/order_api'
        K8S_DEPLOY_FILE = 'order-api-deployment.yaml'
        K8S_SERVICE_FILE = 'order-api-secret.yaml'

        // Your environment variables for testing & deployment
        DB_HOST = 'iit-cc-assignment.cg7k80goqzon.us-east-1.rds.amazonaws.com'
        DB_NAME = 'test_iit_game_service'
        DB_USER = 'appuser_test'
        DB_PASSWORD = 'app_password'
        DB_PORT = '3306'
        COGNITO_USER_POOL_ID = 'us-east-1_SGSijIBP0'
        COGNITO_CLIENT_ID = '79kvjkpkt94sksjel3f0720834'
        AWS_REGION = 'us-east-1'
        OIDC_TOKEN = 'eyJraWQiOiJ1Z1N2T1lOUWY3TUVQWlJFMkNcL3pkMDBGOGMyemZCSW5ITE9OSldDZENBMD0iLCJhbGciOiJSUzI1NiJ9.eyJhdF9oYXNoIjoiZ0FjT0Y5MkU0TkM5cllkaE05R2RxdyIsInN1YiI6IjI0NjhjNDk4LWQwYjEtNzAzMy1iYTk3LWIzMTVlNGRjMWZlZCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9TR1NpaklCUDAiLCJjb2duaXRvOnVzZXJuYW1lIjoiMjQ2OGM0OTgtZDBiMS03MDMzLWJhOTctYjMxNWU0ZGMxZmVkIiwib3JpZ2luX2p0aSI6ImFhODMyMWI0LTNiYjYtNDA5OC05MzRhLTAwNmUzNDFhZDY5MCIsImF1ZCI6Ijc5a3Zqa3BrdDk0c2tzamVsM2YwNzIwODM0IiwiZXZlbnRfaWQiOiI3YThjOTZkYS1hOTlmLTRjMDItYjViMC1mNmUzYTcyZDk2OGYiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTc1MDU3MzcwMCwiZXhwIjoxNzUwNTc3MzAwLCJpYXQiOjE3NTA1NzM3MDAsImp0aSI6IjE3MzA2YWQ2LTQ3ZmQtNDU2Ny05ZWM0LWUzNDk1NmI1YjA4OCIsImVtYWlsIjoiYmx1ZXBob2VuaXg3ODNAZ21haWwuY29tIn0.ioM-Cd0c9z-tt603p8otOu5oGlUjzxUBIeezVs2NKWUXcgeXOWcABHeNP1S4nXkKz1kvXheoXscym9igOQCsDrRTLulbcuubLnJrRi_ddP69mVqM4f3M22DRZQXGA6Qm25BK_0Jx7a9Obo0KPc0T1lEbSH6wZXieVksjy4yJtr196cwrxHq988QzUm6GlHl_0V4Ub_zKCHrYvHYPmruxyY_H1OQ-rfza-OOK2aV1Pr0VSv7oE85rHQY1NVF_7O_roC1b9P4HADDIstKJktRpiHQ6_ZPifxIbrYXKxP3dpcBi3VH0QKEfiWIzKYRcjrB57bTvsK0bQJO1CuVq8LOE7w'
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
                            -p 8091:8081 \\
                            -e DB_HOST=${DB_HOST} \\
                            -e DB_NAME=${DB_NAME} \\
                            -e DB_USER=${DB_USER} \\
                            -e DB_PASSWORD=${DB_PASSWORD} \\
                            -e DB_PORT=${DB_PORT} \\
                            -e COGNITO_USER_POOL_ID=${COGNITO_USER_POOL_ID} \\
                            -e COGNITO_CLIENT_ID=${COGNITO_CLIENT_ID} \\
                            -e AWS_REGION=${AWS_REGION} \\
                            -e OIDC_TOKEN=${OIDC_TOKEN} \\
                            ${DOCKER_HUB_REPO}:latest \\
                            /bin/sh -c "uvicorn app.main:app --host 0.0.0.0 --port 8081 & sleep 15 && pytest app/tests/integration"

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
                        kubectl apply -f ${K8S_SECRET_FILE} --validate=false
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
