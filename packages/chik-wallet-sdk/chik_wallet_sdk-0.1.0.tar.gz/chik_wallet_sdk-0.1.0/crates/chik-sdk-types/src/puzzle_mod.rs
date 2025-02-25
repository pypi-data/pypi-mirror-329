use chik_puzzle_types::{
    cat::{CatArgs, EverythingWithSignatureTailArgs, GenesisByCoinIdTailArgs},
    did::DidArgs,
    nft::{
        NftIntermediateLauncherArgs, NftOwnershipLayerArgs, NftRoyaltyTransferPuzzleArgs,
        NftStateLayerArgs,
    },
    singleton::SingletonArgs,
    standard::StandardArgs,
};
use chik_puzzles::{
    CAT_PUZZLE, CAT_PUZZLE_HASH, DID_INNERPUZ, DID_INNERPUZ_HASH, EVERYTHING_WITH_SIGNATURE,
    EVERYTHING_WITH_SIGNATURE_HASH, GENESIS_BY_COIN_ID, GENESIS_BY_COIN_ID_HASH,
    NFT_INTERMEDIATE_LAUNCHER, NFT_INTERMEDIATE_LAUNCHER_HASH, NFT_OWNERSHIP_LAYER,
    NFT_OWNERSHIP_LAYER_HASH, NFT_OWNERSHIP_TRANSFER_PROGRAM_ONE_WAY_CLAIM_WITH_ROYALTIES,
    NFT_OWNERSHIP_TRANSFER_PROGRAM_ONE_WAY_CLAIM_WITH_ROYALTIES_HASH, NFT_STATE_LAYER,
    NFT_STATE_LAYER_HASH, P2_DELEGATED_PUZZLE_OR_HIDDEN_PUZZLE,
    P2_DELEGATED_PUZZLE_OR_HIDDEN_PUZZLE_HASH, SINGLETON_TOP_LAYER_V1_1,
    SINGLETON_TOP_LAYER_V1_1_HASH,
};
use klvm_traits::ToKlvm;
use klvm_utils::{CurriedProgram, TreeHash, TreeHasher};

pub trait Mod {
    const MOD_REVEAL: &[u8];
    const MOD_HASH: TreeHash;

    fn curry_tree_hash(&self) -> TreeHash
    where
        Self: Sized + ToKlvm<TreeHasher>,
    {
        CurriedProgram {
            program: Self::MOD_HASH,
            args: self,
        }
        .to_klvm(&mut TreeHasher)
        .unwrap()
    }
}

impl<T> Mod for &T
where
    T: Mod,
{
    const MOD_REVEAL: &'static [u8] = T::MOD_REVEAL;
    const MOD_HASH: TreeHash = T::MOD_HASH;
}

impl Mod for StandardArgs {
    const MOD_REVEAL: &[u8] = &P2_DELEGATED_PUZZLE_OR_HIDDEN_PUZZLE;
    const MOD_HASH: TreeHash = TreeHash::new(P2_DELEGATED_PUZZLE_OR_HIDDEN_PUZZLE_HASH);
}

impl<I> Mod for CatArgs<I> {
    const MOD_REVEAL: &[u8] = &CAT_PUZZLE;
    const MOD_HASH: TreeHash = TreeHash::new(CAT_PUZZLE_HASH);
}

impl<I, M> Mod for DidArgs<I, M> {
    const MOD_REVEAL: &[u8] = &DID_INNERPUZ;
    const MOD_HASH: TreeHash = TreeHash::new(DID_INNERPUZ_HASH);
}

impl Mod for NftIntermediateLauncherArgs {
    const MOD_REVEAL: &[u8] = &NFT_INTERMEDIATE_LAUNCHER;
    const MOD_HASH: TreeHash = TreeHash::new(NFT_INTERMEDIATE_LAUNCHER_HASH);
}

impl Mod for NftRoyaltyTransferPuzzleArgs {
    const MOD_REVEAL: &[u8] = &NFT_OWNERSHIP_TRANSFER_PROGRAM_ONE_WAY_CLAIM_WITH_ROYALTIES;
    const MOD_HASH: TreeHash =
        TreeHash::new(NFT_OWNERSHIP_TRANSFER_PROGRAM_ONE_WAY_CLAIM_WITH_ROYALTIES_HASH);
}

impl<I, P> Mod for NftOwnershipLayerArgs<I, P> {
    const MOD_REVEAL: &[u8] = &NFT_OWNERSHIP_LAYER;
    const MOD_HASH: TreeHash = TreeHash::new(NFT_OWNERSHIP_LAYER_HASH);
}

impl<I, M> Mod for NftStateLayerArgs<I, M> {
    const MOD_REVEAL: &[u8] = &NFT_STATE_LAYER;
    const MOD_HASH: TreeHash = TreeHash::new(NFT_STATE_LAYER_HASH);
}

impl<I> Mod for SingletonArgs<I> {
    const MOD_REVEAL: &[u8] = &SINGLETON_TOP_LAYER_V1_1;
    const MOD_HASH: TreeHash = TreeHash::new(SINGLETON_TOP_LAYER_V1_1_HASH);
}

impl Mod for EverythingWithSignatureTailArgs {
    const MOD_REVEAL: &[u8] = &EVERYTHING_WITH_SIGNATURE;
    const MOD_HASH: TreeHash = TreeHash::new(EVERYTHING_WITH_SIGNATURE_HASH);
}

impl Mod for GenesisByCoinIdTailArgs {
    const MOD_REVEAL: &[u8] = &GENESIS_BY_COIN_ID;
    const MOD_HASH: TreeHash = TreeHash::new(GENESIS_BY_COIN_ID_HASH);
}
