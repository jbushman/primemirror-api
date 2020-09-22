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
                switch ( params.distro ) {
                    case "f32":
                        mock_cfg = "fedora-32-x86_64-ul"

                    case "centos7":
                        mock_cfg = "epel-7-x86_64-ul"

                    case "centos6":
                        mock_cfg = "epel-6-x86_64-ul"

                    default:
                        error("Invalid value for distro: ${params.distro}")
                }
            }
        }
    }

    stage('Create tar archive') {
      steps {
            sh """
                mkdir -p /tmp/pmapi
                tar --exclude-vcs --transform='s|^\\./|./pmapi-${env.PKG_VERSION}/|' -cvzf /tmp/pmapi/pmapi-${env.PKG_VERSION}.tar.gz . 
            """
      }
    }


    stage('Generate RPM specfile') {
        steps {
            sh """
                python setup.py bdist_rpm --spec-only
            """
        }
    }

    stage('Build Source RPM') {
      steps {
          sh"""
              mock -r ${mock_cfg} --uniqueext="${JOB_BASE_NAME}:${BUILD_ID}" --buildsrpm --spec dist/pmapi.spec --sources /tmp/pmapi sudo -u mirroradmin cp /var/lib/mock/${mock_cfg}-${JOB_BASE_NAME}:${BUILD_ID}/result/*.src.rpm /tmp/pmapi/
            """
      }
    }

  }
}
