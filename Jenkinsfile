@Library('eigi-jenkins-library')_

def mock_cfg
def distro_str

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
                    distro_str = "fedora32"
                }
                else if ( params.distro  == "centos7") {
                    mock_cfg = "epel-7-x86_64-ul"
                    distro_str = "centos7"
                }
                else if ( params.distro  == "centos6") {
                    mock_cfg = "epel-6-x86_64-ul"
                    distro_str = "centos6"
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

    stage('Collect data from RPM') {
      steps {
          script {
             env.BINARY_RPM = sh(returnStdout: true, script: "cd /tmp/pmapi:${BUILD_ID}; ls pmapi*rpm | grep '\\(noarch\\|x86_64\\)'").trim();
             env.VERSION_STR = sh(returnStdout: true, script: "rpm -qp /tmp/pmapi:${BUILD_ID}/${env.BINARY_RPM} --qf '%{VERSION}\n'").trim()
             env.RELEASE_STR = sh(returnStdout: true, script: "rpm -qp /tmp/pmapi:${BUILD_ID}/${env.BINARY_RPM} --qf '%{RELEASE}\n'").trim()
             env.ARCH_STR = sh(returnStdout: true, script: "rpm -qp /tmp/pmapi:${BUILD_ID}/${env.BINARY_RPM} --qf '%{ARCH}\n'").trim()
             env.SUMMARY_STR = sh(returnStdout: true, script: "rpm -qp /tmp/pmapi:${BUILD_ID}/${env.BINARY_RPM} --qf '%{SUMMARY}\n'").trim()
             env.EPOCH_STR = sh(returnStdout: true, script: "rpm -qp /tmp/pmapi:${BUILD_ID}/${env.BINARY_RPM} --qf '%{EPOCH}\n'").trim()
          }
      }
    }

    stage('Evaluate epoch string') {
        when {
            expression { env.EPOCH_STR == '(none)' }
        }
        steps {
            script {
              env.EPOCH_STR = "0"
            }
        }
    }

    stage('Deploy RPM') {
      steps {
            script{
                def exitCode = sh(returnStatus: true, script: "find /tmp/pmapi:${BUILD_ID}/ -name '*.x86_64.rpm' | egrep .")
                boolean exists = exitCode == 0
                if (exists) {
                    sh """
                    sudo -u mirroradmin cp /tmp/pmapi:${BUILD_ID}/*.x86_64.rpm /var/www/html/alpha/${distro}/x86_64 
                    """  
                }
            }
            script{
                def exitCode = sh(returnStatus: true, script: "find /tmp/pmapi:${BUILD_ID}/ -name '*.noarch.rpm' | egrep .")
                boolean exists = exitCode == 0
                if (exists) {
                    sh """
                    sudo -u mirroradmin cp /tmp/pmapi:${BUILD_ID}/*.noarch.rpm /var/www/html/alpha/${distro}/noarch 
                    """  
                }
            }
            script{
                def exitCode = sh(returnStatus: true, script: "find /tmp/pmapi:${BUILD_ID}/ -name '*.src.rpm' | egrep .")
                boolean exists = exitCode == 0
                if (exists) {
                    sh """
                    sudo -u mirroradmin cp /tmp/pmapi:${BUILD_ID}/*.src.rpm /var/www/html/alpha/${distro}/srpms 
                    """  
                }
            }

      }
    }


    stage('Sign RPM') {
      steps {
          script {
                String requestBody = common.v2.HttpsRequest.toJson([
                    'distro':       "${distro}",
                    'repo':         "alpha",
                    'arch':         "${env.ARCH_STR}",
                    'rpm':          "${env.BINARY_RPM}" ])
                def request = new common.v2.HttpsRequest(this,
                    'http://primemirror.unifiedlayer.com:8001/sign', "POST",
                    ['contentType': 'APPLICATION_JSON'], requestBody)
                def response = request.doHttpsRequest()
                if (response.getStatus() != 200) {
                    echo response.getContent()
                    error ('PrimeMirror API sign call failed.')
                    currentBuild.result = 'FAILURE';
                }
                else {
                    currentBuild.result = 'SUCCESS';
                }
          }
      }
    }
              
    stage('Update yum repo metadata') {
      steps {
        dir("${WORKSPACE}/${PKG_NAME}"){
          sh "sudo -u mirroradmin createrepo --update /var/www/html/alpha/${distro}/"
        }
      }
    }

    stage('Refresh promote service cache') {
      steps {
        dir("${WORKSPACE}/${PKG_NAME}"){
            script {
                if (distro == "centos6" || distro == "centos7") {
                    def curl_out = sh(returnStdout: true, script: "curl --silent https://promote.unifiedlayer.com/recache/${distro}").trim()
                }

            }
        }
      }
    }

    stage('Post data to deployment API') {
        steps {
            script {
                String requestBody = common.v2.HttpsRequest.toJson([
                    'artifact_type_name':   'RPM', 
                    'arch':                 "${env.ARCH_STR}", 
                    'description':          "${env.SUMMARY_STR}", 
                    'epoch':                "${env.EPOCH_STR}", 
                    'name':                 "${env.PKG_NAME}", 
                    'package':              "${env.BINARY_RPM}", 
                    'release':              "${env.RELEASE_STR}", 
                    'version':              "${env.VERSION_STR}",
                    'created_by':           "jenkins" ])
                def request = new common.v2.HttpsRequest(this,
                    'https://deployment.unifiedlayer.com/api/1.0.0/register/rpm', "POST",
                    ['contentType': 'APPLICATION_JSON'], requestBody)
                def response = request.doHttpsRequest()
                if (response.getStatus() != 200 && 
                    response.getStatus() != 201) {
                    echo response.getContent()
                    error ('Deployment API RPM register call failed.')
                    currentBuild.result = 'FAILURE';
                }
                else {
                    currentBuild.result = 'SUCCESS';
                }
            }
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
