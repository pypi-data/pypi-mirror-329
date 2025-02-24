use crate::{DriverError, Spend, SpendContext};

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum MetadataUpdate {
    NewDataUri(String),
    NewMetadataUri(String),
    NewLicenseUri(String),
}

impl MetadataUpdate {
    pub fn spend(&self, ctx: &mut SpendContext) -> Result<Spend, DriverError> {
        let solution = ctx.alloc(&match self {
            Self::NewDataUri(uri) => ("u", uri),
            Self::NewMetadataUri(uri) => ("mu", uri),
            Self::NewLicenseUri(uri) => ("lu", uri),
        })?;
        Ok(Spend::new(ctx.nft_metadata_updater()?, solution))
    }
}
