pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = 'zicofarry'
        BACKEND_IMAGE  = "${DOCKER_HUB_USER}/indie-rock-backend"
        FRONTEND_IMAGE = "${DOCKER_HUB_USER}/indie-rock-frontend"
        BUILD_TAG      = "${BUILD_NUMBER}"
    }

    stages {
        // ============================================
        // Stage 1: Checkout - Ambil kode dari GitHub
        // ============================================
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/zicofarry/TP2DPCC26C2.git'
            }
        }

        // ============================================
        // Stage 2: Build & Push - Bangun image Docker
        //          dan kirim ke Docker Hub
        // ============================================
        stage('Build & Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-login',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    // Login ke Docker Hub
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'

                    // Build & Push Backend Image
                    sh "docker build -t ${BACKEND_IMAGE}:${BUILD_TAG} -t ${BACKEND_IMAGE}:latest ./backend"
                    sh "docker push ${BACKEND_IMAGE}:${BUILD_TAG}"
                    sh "docker push ${BACKEND_IMAGE}:latest"

                    // Build & Push Frontend Image
                    sh "docker build -t ${FRONTEND_IMAGE}:${BUILD_TAG} -t ${FRONTEND_IMAGE}:latest ./frontend"
                    sh "docker push ${FRONTEND_IMAGE}:${BUILD_TAG}"
                    sh "docker push ${FRONTEND_IMAGE}:latest"
                }
            }
        }

        // ============================================
        // Stage 3: Deploy - Update aplikasi di AKS
        //          menggunakan kubeconfig
        // ============================================
        stage('Deploy') {
            steps {
                withCredentials([file(
                    credentialsId: 'aks-config',
                    variable: 'KUBECONFIG'
                )]) {
                    // Apply semua file YAML Kubernetes
                    sh 'kubectl apply -f k8s/'

                    // Force update image agar pod di-restart dengan image terbaru
                    sh "kubectl set image deployment/backend-deployment backend=${BACKEND_IMAGE}:${BUILD_TAG}"
                    sh "kubectl set image deployment/frontend-deployment frontend=${FRONTEND_IMAGE}:${BUILD_TAG}"

                    // Tampilkan status deployment
                    sh 'kubectl rollout status deployment/backend-deployment --timeout=60s'
                    sh 'kubectl rollout status deployment/frontend-deployment --timeout=60s'
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline berhasil! Aplikasi sudah ter-deploy di AKS.'
        }
        failure {
            echo '❌ Pipeline gagal! Cek log untuk detail error.'
        }
    }
}
