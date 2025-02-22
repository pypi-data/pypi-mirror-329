// #include "AttentionWrapper.h"
// //==============================================================================
// using namespace vajra;
// //==============================================================================
// AttentionWrapper::AttentionWrapper(
//     BatchPrefillWithPagedKVCachePyTorchWrapper& wrapper,
//     const std::shared_ptr<ProcessGroupWrapper> spProcessGroupWrapper,
//     int nNumQHeads,
//     int nNumKvHeads,
//     int nHeadDim,
//     int nCacheParallelRank,
//     unsigned int nLayout,
//     float nSoftmaxScale,
//     unsigned int nPosEncodingMode,
//     bool bAllowFp16QKReduction,
//     int nWindowLeft,
//     float nLogitsSoftCap,
//     float nRopeScale,
//     float nRopeTheta,
//     bool bSkipAttentionReduction)
//     : m_wrapper(wrapper),
//       m_bBeginForwardCalled(false),
//       m_spProcessGroupWrapper(spProcessGroupWrapper),
//       m_nNumQHeads(nNumQHeads),
//       m_nNumKvHeads(nNumKvHeads),
//       m_nHeadDim(nHeadDim),
//       m_nCacheParallelRank(nCacheParallelRank),
//       m_nLayout(nLayout),
//       m_nSoftmaxScale(nSoftmaxScale),
//       m_nPosEncodingMode(nPosEncodingMode),
//       m_bAllowFp16QKReduction(bAllowFp16QKReduction),
//       m_nWindowLeft(nWindowLeft),
//       m_nLogitsSoftCap(nLogitsSoftCap),
//       m_nRopeScale(nRopeScale),
//       m_nRopeTheta(nRopeTheta),
//       m_bSkipAttentionReduction(bSkipAttentionReduction),
//       bShouldPrintLog(false)
// {
// }
// //==============================================================================
// void AttentionWrapper::BeginForward(
//     bool bContainsMultiGroupPrefillSeq,
//     bool bContainsMultiGroupDecodeSeq,
//     unsigned int nMultiGroupSeqPrefillLen,
//     const std::set<int>& vMultiGroupSeqGroupIds,
//     const torch::Tensor& qoIndptr,
//     const torch::Tensor& kvIndptr,
//     const torch::Tensor& kvIndices,
//     const torch::Tensor& kvLastPageLen)
// {
//   ASSERT(!m_bBeginForwardCalled);

//   ASSERT(!(bContainsMultiGroupPrefillSeq && bContainsMultiGroupDecodeSeq));

//   if (bContainsMultiGroupPrefillSeq)
//   {
//     ASSERT(nMultiGroupSeqPrefillLen > 0);
//     ASSERT(!vMultiGroupSeqGroupIds.empty());
//   }

//   if (bContainsMultiGroupDecodeSeq)
//   {
//     ASSERT(!vMultiGroupSeqGroupIds.empty());
//   }

//   m_bBeginForwardCalled = true;

//   m_bContainsMultiGroupPrefillSeq = bContainsMultiGroupPrefillSeq;
//   m_bContainsMultiGroupDecodeSeq = bContainsMultiGroupDecodeSeq;
//   m_nMultiGroupSeqPrefillLen = nMultiGroupSeqPrefillLen;
//   m_vMultiGroupSeqGroupIds = vMultiGroupSeqGroupIds;
//   m_qoIndptr = qoIndptr;
//   m_kvIndptr = kvIndptr;
//   m_kvIndices = kvIndices;
//   m_kvLastPageLen = kvLastPageLen;
// }
// //==============================================================================
// void AttentionWrapper::EndForward()
// {
//   ASSERT(m_bBeginForwardCalled);

//   m_bBeginForwardCalled = false;
// }
// //==============================================================================
// std::vector<torch::Tensor> AttentionWrapper::Forward(
//     float nSoftmaxScale /*[in]*/,
//     const torch::Tensor& q /*[in]*/,
//     const torch::Tensor& kvCache /*[inout]*/,
//     bool bCausal /*[in]*/
// )
// {
//   auto outputAndLse = m_wrapper.Run(
//       q,
//       m_qoIndptr,
//       kvCache,
//       std::nullopt /*paged_k_cache*/,
//       std::nullopt /*paged_v_cache*/,
//       m_kvIndptr,
//       m_kvIndices,
//       m_kvLastPageLen,
//       bCausal,
//       m_nPosEncodingMode,
//       m_bAllowFp16QKReduction,
//       m_nWindowLeft,
//       m_nLogitsSoftCap,
//       nSoftmaxScale,
//       m_nRopeScale,
//       m_nRopeTheta,
//       true /*return_lse*/
//   );
//   return outputAndLse;
// }
// //==============================================================================
// torch::Tensor AttentionWrapper::GatherTensor(
//     const torch::Tensor& output,
//     const torch::Tensor& S,
//     bool bContainsMultiGroupPrefillSeq,
//     bool bContainsMultiGroupDecodeSeq,
//     unsigned int nMultiGroupSeqPrefillLen,
//     const std::set<int>& vMultiGroupSeqGroupIds)
// {
//   if (m_bContainsMultiGroupPrefillSeq)
//   {
//     auto processGroup = m_spProcessGroupWrapper->GetCacheModelParallelGroup(
//         m_vMultiGroupSeqGroupIds);
//     auto vMultiGroupV =
//         output.slice(0, 0, m_nMultiGroupSeqPrefillLen).unsqueeze(1);
//     auto bMultiGroupS = S.slice(0, 0,
//     m_nMultiGroupSeqPrefillLen).unsqueeze(1);

//     vMultiGroupV = ParallelOps::GatherFromCacheModelParallelRegion(
//         vMultiGroupV,
//         m_nCacheParallelRank,
//         processGroup);
//     bMultiGroupS = ParallelOps::GatherFromCacheModelParallelRegion(
//         bMultiGroupS,
//         m_nCacheParallelRank,
//         processGroup);

//     auto mergedOutput = merge_states(vMultiGroupV, bMultiGroupS);
//     output.slice(0, 0, m_nMultiGroupSeqPrefillLen) = mergedOutput[0];
//   }
//   else if (m_bContainsMultiGroupDecodeSeq)
//   {
//     auto processGroup = m_spProcessGroupWrapper->GetCacheModelParallelGroup(
//         m_vMultiGroupSeqGroupIds);
//     auto vMultiGroupV = output.slice(0, -1).unsqueeze(0);
//     auto vMultiGroupS = S.slice(0, -1).unsqueeze(0);

//     vMultiGroupV = ParallelOps::GatherFromCacheModelParallelRegion(
//         vMultiGroupV,
//         m_nCacheParallelRank,
//         processGroup);
//     vMultiGroupS = ParallelOps::GatherFromCacheModelParallelRegion(
//         vMultiGroupS,
//         m_nCacheParallelRank,
//         processGroup);

//     auto mergedOutput = merge_states(vMultiGroupV, vMultiGroupS);
//     output.slice(0, -1) = mergedOutput[0];
//   }

//   return output;
// }
// //==============================================================================