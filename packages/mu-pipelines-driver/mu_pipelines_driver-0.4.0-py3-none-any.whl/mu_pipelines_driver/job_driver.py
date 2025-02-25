from mu_pipelines_driver.ioc.ioc_container import IOCContainer


def job_driver(ioc_container: IOCContainer) -> object | None:
    last_df: object | None = None

    for exec_module in ioc_container.execute_modules:
        last_df = exec_module.execute(ioc_container.context)

    for dest_module in ioc_container.destination_modules:
        dest_module.save(last_df, ioc_container.context)

    return last_df
