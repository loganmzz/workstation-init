#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import json

def get_component(module,gcloud_bin_path):
    component_id=module.params['name']
    rc, stdout, stderr = module.run_command(
        [
            gcloud_bin_path,
            'components',
            'list',
            '--format',
            'json',
            '--filter',
            f'id={component_id}',
        ],
        check_rc=True,
    )
    components=json.loads(stdout)
    if len(components) == 0:
        module.fail_json({'msg': 'No component found'})
    elif len(components) > 1:
        module.fail_json({'msg': 'Too many components found', 'state': components})

    return components[0]


def run_module():
    result = {
        'changed': False,
    }

    module = AnsibleModule(
        argument_spec={
            'name': {
                'type': 'str',
                'required': True,
            },
            'state': {
                'type': 'str',
                'required': False,
                'default': 'present',
            },
        },
    )

    action_before=''
    action_after=''
    action_command=''
    param_state=module.params['state']
    if param_state == 'present':
        action_before='Not Installed'
        action_after='Installed'
        action_command='install'
    elif param_state == 'absent':
        action_before='Installed'
        action_after='Not Installed'
        action_command='remove'
    else:
        module.fail_json({'msg': f'Unsupported state {param_state}'})

    gcloud_bin_path=module.get_bin_path('gcloud', True)
    result['executable']=gcloud_bin_path

    component=get_component(module,gcloud_bin_path)
    if component['state']['name'] == action_before:
        rc, stdout, stderr = module.run_command(
            [
                gcloud_bin_path,
                'components',
                action_command,
                module.params['name'],
            ],
            check_rc=True,
        )
        result['stdout']=stdout
        result['stderr']=stderr
        component=get_component(module,gcloud_bin_path)
        result['state']=component
        if component['state']['name'] != action_after:
            module.fail_json(msg=f'Component {action_command} has failed', **result)
        else:
            result['changed']=True
    elif component['state']['name'] == action_after:
        result['state']=component
    else:
        actual_state=component['state']['name']
        module.fail_json(msg=f'Unsupported component state {actual_state}', **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()