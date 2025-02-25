use std::sync::Arc;

use crate::ops::sdk::*;

#[derive(Debug, Deserialize)]
pub struct Spec {
    model: String,
}

struct Executor {
    spec: Spec,
}

#[async_trait]
impl SimpleTransformExecutor for Executor {
    async fn evaluate(&self, _input: Vec<Value>) -> Result<Value> {
        // TODO: Implement the real embedding logic.
        Ok(vec![0.5; 384].into())
    }
}

pub struct Factory;

#[async_trait]
impl SimpleTransformFactoryBase for Factory {
    type Spec = Spec;

    fn name(&self) -> &str {
        "Embed"
    }

    fn get_output_schema(
        &self,
        spec: &Spec,
        input_schema: &Vec<OpArgSchema>,
        _context: &FlowInstanceContext,
    ) -> Result<EnrichedValueType> {
        match &expect_input_1(input_schema)?.value_type.typ {
            ValueType::Basic(BasicValueType::Str) => {}
            t => {
                api_bail!("Expect String as input type, got {}", t)
            }
        }
        if spec.model != "Xenova/all-MiniLM-L6-v2" {
            api_bail!("Unsupported model: {}", spec.model);
        }
        // TODO: Support various embedding models.
        Ok(make_output_type(BasicValueType::Vector(VectorTypeSchema {
            element_type: Box::new(BasicValueType::Float32),
            dimension: Some(384),
        })))
    }

    async fn build_executor(
        self: Arc<Self>,
        spec: Spec,
        _input_schema: Vec<OpArgSchema>,
        _context: Arc<FlowInstanceContext>,
    ) -> Result<Box<dyn SimpleTransformExecutor>> {
        Ok(Box::new(Executor { spec }))
    }
}
