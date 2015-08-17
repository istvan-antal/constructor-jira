def build(infrastructure):
    instance = infrastructure.create_instance('jira')
    instance.provision()

    mysql = instance.create_mysql('jira')
    mysql.create_db_with_user('jira', 'jira', 'jira')

    instance.install('nginx')
    instance.use_nginx_config('nginx.conf')

    instance.upload_file('response.varfile')

    instance.run_commands(
        'wget https://www.atlassian.com/software/jira/downloads/binary/atlassian-jira-6.4.10-x64.bin',
        'chmod +x atlassian-jira-6.4.10-x64.bin',
        'sudo ./atlassian-jira-6.4.10-x64.bin -q -varfile response.varfile'
    )

    instance.upload_file('server.xml')

    instance.run_commands(
        'sudo service jira stop',
        'sudo cp server.xml /opt/atlassian/jira/conf/server.xml',
        'sudo service jira start'
    )

    instance.install_my_key()

