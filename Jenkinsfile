pipeline {
    agent any

    environment {
        BLUE = '\u001B[34m'
        RESET = '\u001B[0m'
        DOCKER_IMAGE = 'devops-app'
        CLUSTER_URL = 'https://your-k8s-api-server:6443'
        CLUSTER_NAMESPACE = 'default'
    }

    parameters {
        string(name: 'APP_VERSION', defaultValue: '1.0', description: 'Қолданба версиясы')
        choice(name: 'TEST_LEVEL', choices: ['basic', 'full'], description: 'Тест деңгейі')
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "${BLUE}GitHub-тан код алу${RESET}"
                }
                checkout scm
                sh 'ls -la'
            }
        }

        stage('Build Java App') {
            steps {
                script {
                    echo "Maven арқылы build..."
                    echo "APP_VERSION = ${params.APP_VERSION}"

                    docker.image('maven:3.8-openjdk-11').inside {
                        sh 'mvn clean package'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Docker образын құрастыру..."
                    sh """
                        docker build -t ${DOCKER_IMAGE}:${params.APP_VERSION} .
                        docker tag ${DOCKER_IMAGE}:${params.APP_VERSION} ${DOCKER_IMAGE}:latest
                        docker images | head -5
                    """
                }
            }
        }

        stage('Start Services') {
            steps {
                script {
                    echo "Docker Compose сервистерін іске қосу..."
                    sh '''
                        docker-compose down -v || true
                        docker-compose up -d
                        echo "Сервистердің іске қосылуын күту... (20 секунд)"
                        sleep 20
                        docker-compose ps
                    '''
                }
            }
        }

        stage('Test API') {
            steps {
                script {
                    try {
                        if (params.TEST_LEVEL == 'basic') {
                            sh '''
                                CONTAINER_ID=$(docker-compose ps -q app)
                                echo "Container ID: $CONTAINER_ID"

                                RESPONSE=$(docker exec "$CONTAINER_ID" sh -c "python - <<'PY'
import urllib.request
data = urllib.request.urlopen('http://127.0.0.1:5000/').read().decode()
print(data)
PY")
                                echo "Жауап: $RESPONSE"
                                echo "$RESPONSE" | grep -E "hits|message"
                            '''
                        } else {
                            sh '''
                                CONTAINER_ID=$(docker-compose ps -q app)
                                echo "Container ID: $CONTAINER_ID"

                                RESPONSE=$(docker exec "$CONTAINER_ID" sh -c "python - <<'PY'
import urllib.request
data = urllib.request.urlopen('http://127.0.0.1:5000/').read().decode()
print(data)
PY")
                                echo "Жауап: $RESPONSE"
                                echo "$RESPONSE" | grep -E "hits|message"

                                docker exec "$CONTAINER_ID" sh -c "python - <<'PY'
import urllib.request

urls = [
    'http://127.0.0.1:5000/add-user?name=JenkinsUser1',
    'http://127.0.0.1:5000/add-user?name=JenkinsUser2',
    'http://127.0.0.1:5000/add-user?name=JenkinsUser3',
    'http://127.0.0.1:5000/users'
]

for url in urls:
    try:
        print(urllib.request.urlopen(url).read().decode())
    except Exception as e:
        print(f'Error: {e}')
PY"
                            '''
                        }
                    } catch (Exception e) {
                        currentBuild.result = 'UNSTABLE'
                        echo "Тесттер тұрақсыз, бірақ пайплайн жалғасады"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            when {
                branch 'main'
            }
            steps {
                script {
                    echo "Kubernetes-ке deploy басталды..."
                }
                withKubeConfig([credentialsId: 'kubernetes-creds',
                                serverUrl: "${CLUSTER_URL}",
                                namespace: "${CLUSTER_NAMESPACE}"]) {
                    sh 'kubectl apply -f redis-deployment.yaml'
                    sh 'kubectl apply -f app-deployment.yaml'
                    sh 'kubectl rollout status deployment/java-app-deployment'
                }
            }
        }
    }

    post {
        always {
            script {
                echo "Тазалау жұмыстары..."
                sh 'docker-compose down -v || true'
            }
        }

        success {
            echo 'ПАЙПЛАЙН СӘТТІ АЯҚТАЛДЫ!'
        }

        unstable {
            echo 'ПАЙПЛАЙН UNSTABLE КҮЙІМЕН АЯҚТАЛДЫ!'
        }

        failure {
            echo 'ПАЙПЛАЙН ҚАТЕМЕН АЯҚТАЛДЫ!'
            sh '''
                docker-compose ps || true
                docker-compose logs app || true
            '''
        }
    }
}
