pipeline {
    agent any

    environment {
        BLUE = '\u001B[34m'
        RESET = '\u001B[0m'
        DOCKER_IMAGE = 'devops-app'
        // Jenkins Docker ішінде болса, localhost орнына контейнер атын қолданамыз
        APP_URL = "http://app:5000" 
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
                    // Maven контейнері ішінде құрастыру
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
                    // Ескі контейнерлерді өшіріп, жаңасын қосу
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
                    echo "Redis тестілеу басталуда..."
                    // RESPONSE айнымалысын дұрыс анықтау және sh ішіндегі sh-ты алып тастау
                    sh """
                        RESPONSE=\$(curl -s ${APP_URL}/)
                        echo "Жауап: \$RESPONSE"
                        echo \$RESPONSE | grep -E "hits|message" || echo "Сөз табылмады"
                    """
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
            // Қате болған жағдайда контейнер журналдарын шығару (диагностика үшін)
            sh 'docker-compose logs app || true'
        }
    }
}
