pipeline {
    agent any

    environment {
        BLUE = '\u001B[34m'
        RESET = '\u001B[0m'
        DOCKER_IMAGE = 'devops-app'
        APP_URL = 'http://localhost:5000'
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
                    sh "docker build -t ${DOCKER_IMAGE}:latest ."
                }
            }
        }

        stage('Start Services') {
            steps {
                script {
                    echo "Docker Compose сервистерін іске қосу..."
                    sh 'docker-compose down -v || true'
                    sh 'docker-compose up -d'
                    echo "Сервистердің іске қосылуын күту... (20 секунд)"
                    sleep 20
                    sh 'docker-compose ps'
                }
            }
        }

        stage('Test Redis') {
    steps {
        script {
            sh '''
                RESPONSE=$(docker exec $(docker-compose ps -q app) python - <<'PY'
import urllib.request
print(urllib.request.urlopen("http://127.0.0.1:5000/").read().decode())
PY
)
                echo "$RESPONSE"
                echo "$RESPONSE" | grep -E "hits|message"
            '''
        }
    }
}

        stage('Test PostgreSQL') {
            steps {
                script {
                    echo "PostgreSQL тестілеу..."
                    sh """
                        curl -s "${APP_URL}/add-user?name=JenkinsUser1"
                        curl -s "${APP_URL}/add-user?name=JenkinsUser2"
                        curl -s "${APP_URL}/add-user?name=JenkinsUser3"
                        echo "Пайдаланушылар тізімі:"
                        curl -s ${APP_URL}/users
                    """
                }
            }
        }

        stage('Test Client') {
            steps {
                script {
                    echo "Python клиентін тестілеу..."
                    sh 'docker-compose run --rm client || echo "Клиент қатемен аяқталды"'
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
        failure {
            echo 'ПАЙПЛАЙН ҚАТЕМЕН АЯҚТАЛДЫ!'
            sh 'docker-compose logs app || true'
        }
    }
}
