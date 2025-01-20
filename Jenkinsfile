pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'image-to-pdf-converter'
        GITHUB_REPO = 'https://github.com/mallelavamshi/john.git'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: "${env.GITHUB_REPO}"
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE:$BUILD_NUMBER .'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    sh '''
                        docker stop $DOCKER_IMAGE || true
                        docker rm $DOCKER_IMAGE || true
                        docker run -d --name $DOCKER_IMAGE \
                            -p 8501:8501 \
                            --restart unless-stopped \
                            $DOCKER_IMAGE:$BUILD_NUMBER
                    '''
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    sh '''
                        sleep 15
                        curl -f http://localhost:8501 || exit 1
                    '''
                }
            }
        }
    }
    
    post {
        failure {
            script {
                sh '''
                    docker logs $DOCKER_IMAGE
                    docker stop $DOCKER_IMAGE || true
                    docker rm $DOCKER_IMAGE || true
                '''
            }
        }
        always {
            // Clean up old images
            sh 'docker system prune -f'
        }
    }
}