pipeline { 

    agent any 
    stages { 
        stage('Checkout Code') { 

            steps { 
                echo 'Забираем код из GitHub...' 

                checkout scm 

            } 
        } 
        stage('Check Files') { 

            steps { 

                echo '📄 Проверяем созданные файлы...' 

                sh ''' 

                    echo "=== ФАЙЛЫ В РЕПОЗИТОРИИ ===" 

                    ls -la 

                    echo "" 

                    echo "=== ПРОВЕРКА НАШИХ ФАЙЛОВ ===" 

                    if [ -f Dockerfile ]; then 

                        echo "Dockerfile найден" 

                        echo "Содержимое Dockerfile:" 

                        head -10 Dockerfile 

                    else 

                        echo "Dockerfile не найден" 

                    fi 

                     

                    if [ -f requirements.txt ]; then 

                        echo "requirements.txt найден" 

                    else 

                        echo "requirements.txt не найден" 

                    fi 

                     

                    if [ -d src ]; then 

                        echo "Папка src найдена" 

                        if [ -f src/app.py ]; then 

                            echo "Файл src/app.py найден" 

                        else 

                            echo "Файл src/app.py не найден" 

                        fi 

                    else 

                        echo "Папка src не найдена" 

                    fi 

                     

                    if [ -f .dockerignore ]; then 

                        echo ".dockerignore найден" 

                    else 

                        echo ".dockerignore не найден" 

                    fi 

                ''' 

            } 

        } 
        stage('Docker Theory') { 

            steps { 

                echo 'ТЕОРИЯ DOCKER' 

                echo 'Если бы Jenkins не был в Docker, мы бы выполнили:' 

                echo '1. docker build -t my-app .' 

                echo '2. docker run -d -p 8081:5000 my-app' 

                echo '3. curl http://localhost:8081/health' 

                echo '' 

                echo 'Но так как Jenkins в Docker, эти команды могут не работать.' 

                echo 'Это нормально! Главное - понять процесс.' 

            } 

        } 

         

        // СТАДИЯ 4: Попробуем Docker команды (не обязательно) 

        stage('Try Docker Commands') { 

            steps { 

                echo '🔧 Пробуем Docker команды...' 

                script { 

                    try { 

                        // Пробуем проверить Docker 

                        sh 'docker --version || echo "Docker не доступен"' 

                         

                        // Пробуем собрать образ (может не работать) 

                        sh ''' 

                            echo "Пробуем собрать Docker образ..." 

                            docker build -t test-image . 2>/dev/null || echo "Не удалось собрать образ" 

                        ''' 

                    } catch (Exception e) { 

                        echo "Docker команды не работают. Это ожидаемо!" 

                        echo "Причина: Jenkins запущен внутри Docker контейнера" 

                    } 

                } 

            } 

        } 

    } 

     

    post { 

        always { 

            echo ' === ИТОГ РАБОТЫ ===' 

            sh ''' 

                echo "Дата: $(date)" 

                echo "Процесс CI/CD понятен?" 

                echo "1. Код → GitHub" 

                echo "2. GitHub → Jenkins" 

                echo "3. Jenkins проверяет файлы" 

                echo "4. Docker теория изучена" 

            ''' 
        } 
        success { 
            echo 'ОТЛИЧНО! Вы поняли процесс CI/CD!' 
            echo 'Даже если Docker не работал - вы молодец!' 
            echo 'На следующем уроке настроим Docker правильно.' 

        } 
        failure { 
            echo 'Были ошибки, но это часть обучения!' 
            echo 'Главное - файлы созданы и процесс понят.' 

        } 
    } 
} 