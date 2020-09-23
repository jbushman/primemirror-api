@Library('eigi-jenkins-library')_

def mock_cfg

pipeline {
  agent {label 'mockbuild'}
  parameters {
    choice(
        name:       'distro',
        choices:    ['f32', 'centos7', 'centos6'],
        description:'Target Linux distribution'
    )
  }

  environment {
    PKG_VERSION = sh(returnStdout: true, script: "python setup.py --version").trim()

  }

  stages {
    stage('Set mock configuration') {
        steps {
            script {
                echo "The distro param is " + params.distro
                if ( params.distro  == "f32") {
                    mock_cfg = "fedora-32-x86_64-ul"
                }
                else if ( params.distro  == "centos7") {
                    mock_cfg = "epel-7-x86_64-ul"
                }
                else if ( params.distro  == "centos6") {
                    mock_cfg = "epel-6-x86_64-ul"
                }
                else {
                    error("Invalid value for distro: ${params.distro}")
                }
            }
        }
    }

    stage('Create tar archive') {
      steps {
            sh """
                mkdir -p /tmp/pmapi:${BUILD_ID}
                tar --exclude-vcs --transform='s|^\\./|./pmapi-${env.PKG_VERSION}/|' -cvzf /tmp/pmapi:${BUILD_ID}/pmapi-${env.PKG_VERSION}.tar.gz . 
            """
      }
    }


    stage('Generate RPM spec file') {
        steps {
            sh """
                python setup.py bdist_rpm --spec-only
            """
        }
    }

    stage('Patch RPM spec file') {
        steps {
            sh """
              perl -pi -E 'if(/\\%description/) { say "Requires:\\t(\$_)\\nBuildRequires:\\t(\$_)" for qw(python3 python3-setuptools); say ""}' dist/pmapi.spec
 
            """
        }
    }


    stage('Build Source RPM') {
      steps {
          sh"""
              mock -r ${mock_cfg} --uniqueext="${JOB_BASE_NAME}:${BUILD_ID}" --buildsrpm --spec dist/pmapi.spec --sources /tmp/pmapi:${BUILD_ID}
              cp /var/lib/mock/${mock_cfg}-${JOB_BASE_NAME}:${BUILD_ID}/result/*.src.rpm /tmp/pmapi:${BUILD_ID}/
            """
      }
    }

    stage('Build binary RPM') {
        steps {
            sh "mock -r ${mock_cfg} --uniqueext='${JOB_BASE_NAME}:${BUILD_ID}' /tmp/pmapi:${BUILD_ID}/*src.rpm "
            sh "cp /var/lib/mock/${mock_cfg}-${JOB_BASE_NAME}:${BUILD_ID}/result/pmapi*noarch.rpm /tmp/pmapi:${BUILD_ID}" 
        }
    }

  }

  post {
      always {
          script {
              sh """
                  rm -rf /tmp/pmapi:${BUILD_ID}
              """
              echo "Pipeline result: ${currentBuild.result}"
              echo "Pipeline currentResult: ${currentBuild.currentResult}"
              notifyBitbucket()
          }
      }
  }

}
