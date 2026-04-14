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
            docker.image('maven:3.8-openjdk-11').inside {
                sh '''
                    echo "Қолданбаны құрастыру..."
                    mvn clean package
                '''
            }
        }
    }
}

        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                        echo "Docker образын құрастыру..."
                        docker build -t ${DOCKER_IMAGE} .
                        docker tag ${DOCKER_IMAGE} devops-app:latest
                        docker images | head -5
                    """
                }
            }
        }

        stage('Start Services') {
            steps {
                script {
                    sh '''
                        echo "Docker Compose сервистерін іске қосу..."
                        docker-compose down -v || true
                        docker-compose up -d
                        echo "Сервистердің іске қосылуын күту... (20 секунд)"
                        sleep 20
                        docker-compose ps
                    '''
                }
            }
        }

        stage('Test Redis') {
            steps {
                script {
                    sh '''
                        echo "Redis тестілеу..."

                        for i in 1 2 3; do
                            echo "Сұрау $i:"
                            sh 'curl -s http://localhost:5000/ | grep -E "hits|message" || true'
                            sleep 1
                        done

                        echo "Redis ақпараты:"
                        curl -s http://localhost:5000/redis | python -m json.tool
                    '''
                }
            }
        }

        stage('Test PostgreSQL') {
            steps {
                script {
                    sh '''
                        echo "PostgreSQL тестілеу..."

                        curl -s "http://localhost:5000/add-user?name=JenkinsUser1"
                        curl -s "http://localhost:5000/add-user?name=JenkinsUser2"
                        curl -s "http://localhost:5000/add-user?name=JenkinsUser3"

                        echo "Пайдаланушылар тізімі:"
                        curl -s http://localhost:5000/users | python -m json.tool
                    '''
                }
            }
        }

        stage('Test Client') {
            steps {
                script {
                    sh '''
                        echo "Python клиентін тестілеу..."
                        docker-compose run --rm client || echo "Клиент қатемен аяқталды"
                    '''
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    sh '''
                        echo "Тазалау..."
                        docker-compose down -v || true
                        echo "Контейнерлер тазаланды"
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Тазалау жұмыстары"
            sh 'docker-compose down -v || true'
        }

        success {
            echo 'ПАЙПЛАЙН СӘТТІ АЯҚТАЛДЫ!'
        }

        failure {
            echo 'ПАЙПЛАЙН ҚАТЕМЕН АЯҚТАЛДЫ!'
            echo 'Қателерді тексеріңіз'
        }
    }
}
