from _api import *

import inspect

def valid_functions(function, *args):
    if function != inspect.stack()[0][3]:
        params = ', '.join([str(arg) for arg in args[0]])

        cmd = f'{function}({params})'
        print(f"ERROR : {cmd}")

        print("------")

    functions='''
    get_alerts(project_id, unread=False)

    get_builds(user_id)

    get_deployments(project_id, limit=True)

    get_master_token(project_id)

    get_metadata(project_id, set_domain='')

    get_plans()

    get_project_service(project_id, service_id='liferay')

    get_scale(project_id, service_id='liferay')

    get_usage(user_uid)

    get_user(user_id)

    get_user_plans()

    get_user_uid(user_id)

    list_project_service(project_id)

    restart_project_service(project_id, service_id)

    stop_project_service(project_id, service_id)
    '''

    print(functions)

def run_function(function, *args):
    try:
        if args:
            return str(globals()[function](*args))
        else:
            return str(globals()[function](function))
    except:
        if args:
            valid_functions(function, *args)
        else:
            valid_functions(function)

        raise SystemExit

def controller():
    if ARGS:
        output = run_function(FUNCTION, *ARGS)
    else:
        output = run_function(FUNCTION)

    if PRINT_OUTPUT:
        print(output)

    if WRITE_OUTPUT:
        write_file(WRITE_FILE, output)

if __name__ == "__main__":
    controller()