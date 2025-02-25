use super::{
    factory_bases::*, registry::ExecutorFactoryRegistry, sdk::ExecutorFactory, sources, storages,
    transforms,
};
use anyhow::Result;
use std::sync::{Arc, LazyLock, RwLock, RwLockReadGuard};

fn register_executor_factories(registry: &mut ExecutorFactoryRegistry) -> Result<()> {
    sources::local_file::Factory.register(registry)?;

    transforms::embed::Factory.register(registry)?;
    transforms::split_recursively::Factory.register(registry)?;

    Arc::new(storages::postgres::Factory::default()).register(registry)?;

    Ok(())
}

static EXECUTOR_FACTORY_REGISTRY: LazyLock<RwLock<ExecutorFactoryRegistry>> = LazyLock::new(|| {
    let mut registry = ExecutorFactoryRegistry::new();
    register_executor_factories(&mut registry).expect("Failed to register executor factories");
    RwLock::new(registry)
});

pub fn executor_factory_registry() -> RwLockReadGuard<'static, ExecutorFactoryRegistry> {
    EXECUTOR_FACTORY_REGISTRY.read().unwrap()
}

pub fn register_factory(name: String, factory: ExecutorFactory) -> Result<()> {
    let mut registry = EXECUTOR_FACTORY_REGISTRY.write().unwrap();
    registry.register(name, factory)
}
