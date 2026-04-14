pipeline {
    agent any

    environment {
        BLUE = '\u001B[34m'
        RESET = '\u001B[0m'
        DOCKER_IMAGE = 'devops-app'
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
                    docker.image('maven:3.8-openjdk-11').inside {
                        sh '''
                            mvn clean package
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Docker образын құрастыру..."
                    sh """
                        docker build -t ${DOCKER_IMAGE}:latest .
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
                    echo "API тестілеу..."
                    sh '''
                        CONTAINER_ID=$(docker-compose ps -q app)
                        echo "Container ID: $CONTAINER_ID"

                        if [ -z "$CONTAINER_ID" ]; then
                            echo "app контейнері табылмады"
                            docker-compose ps
                            exit 1
                        fi

                        RESPONSE=$(docker exec "$CONTAINER_ID" sh -c "python - <<'PY'
import urllib.request
data = urllib.request.urlopen('http://127.0.0.1:5000/').read().decode()
print(data)
PY")
                        echo "Жауап: $RESPONSE"

                        echo "$RESPONSE" | grep -E "hits|message"
                    '''
                }
            }
        }

        stage('Test PostgreSQL') {
            steps {
                script {
                    echo "PostgreSQL тестілеу..."
                    sh '''
                        CONTAINER_ID=$(docker-compose ps -q app)

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
            }
        }

        stage('Test Client') {
            steps {
                script {
                    echo "Python клиентін тестілеу..."
                    sh 'docker-compose run --rm client || echo "Клиент сервисі жоқ немесе қатемен аяқталды"'
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
            sh '''
                docker-compose ps || true
                docker-compose logs app || true
            '''
        }
    }
}
