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
// MultiAttentionWrapper::MultiAttentionWrapper(
//     AttentionWrapper& prefill_wrapper,
//     AttentionWrapper& decode_wrapper,
//     AttentionWrapper& multi_group_wrapper,
//     int nNumQHeads,
//     int nNumKvHeads,
//     int nHeadDim,
//     int nCacheParallelRank)
//     : m_prefill_wrapper(prefill_wrapper),
//       m_decode_wrapper(decode_wrapper),
//       m_multi_group_wrapper(multi_group_wrapper),
//       m_nNumQHeads(nNumQHeads),
//       m_nNumKvHeads(nNumKvHeads),
//       m_nHeadDim(nHeadDim),
//       m_nCacheParallelRank(nCacheParallelRank)
// {
// }
// //==============================================================================
// void MultiAttentionWrapper::BeginForward(
//     bool bContainsMultiGroupPrefillSeq /*[in]*/,
//     bool bContainsMultiGroupDecodeSeq /*[in]*/,
//     unsigned int nMultiGroupSeqPrefillLen /*[in]*/,
//     const std::set<int>& vMultiGroupSeqGroupIds /*[in]*/,
//     const int nNumPrefillTokens /*[in]*/,
//     const int nNumDecodeTokens /*[in]*/
// )
// {
//   m_bContainsMultiGroupPrefillSeq = bContainsMultiGroupPrefillSeq;
//   m_bContainsMultiGroupDecodeSeq = bContainsMultiGroupDecodeSeq;
//   m_nMultiGroupSeqPrefillLen = nMultiGroupSeqPrefillLen;
//   m_vMultiGroupSeqGroupIds = vMultiGroupSeqGroupIds;
//   m_nNumPrefillTokens = nNumPrefillTokens;
//   m_nNumDecodeTokens = nNumDecodeTokens;
// }
// //==============================================================================
// void MultiAttentionWrapper::SetProfileIteration()
// {
//   m_bIsProfileIteration = true;
// }
// //==============================================================================
// void MultiAttentionWrapper::EndForward()
// {
//   m_bIsProfileIteration = false;
//   m_nNumPrefillTokens = 0;
//   m_nNumDecodeTokens = 0;
//   m_bContainsMultiGroupPrefillSeq = false;
//   m_bContainsMultiGroupDecodeSeq = false;
//   m_nMultiGroupSeqPrefillLen = 0;
//   m_vMultiGroupSeqGroupIds.clear();
// }
// //==============================================================================
// torch::Tensor MultiAttentionWrapper::Forward(
//     float nSoftmaxScale /*[in]*/,
//     const torch::Tensor& q /*[in]*/,
//     const torch::Tensor& k /*[in]*/,
//     const torch::Tensor& v /*[in]*/,
//     const torch::Tensor& kvCache /*[inout]*/
// )
// {
//   if (m_bIsProfileIteration)
//   {
//     return q;
//   }

//   auto output =
//       torch::zeros({q.size(0), m_nNumQHeads, m_nHeadDim}, q.options());
//   auto S = torch::zeros({q.size(0), m_nNumQHeads}, q.options());

//   auto _q = q.contiguous().reshape({-1, m_nNumQHeads, m_nHeadDim});
//   auto appendKey = k.contiguous().reshape({-1, m_nNumKvHeads, m_nHeadDim});
//   auto appendValue = v.contiguous().reshape({-1, m_nNumKvHeads, m_nHeadDim});

//   // TODO(Amey): Add back the append logic using flashinfer 0.2.0

//   // if contains multi group sequence and is not the last rank, then handle
//   the
//   // kv query.
//   //    - if prefill, then slice away the first tokens with length of
//   multigroup
//   //    prefill len.
//   //    - if decode, then slice away the last token
//   // if (!m_bShouldMultiGroupAppendKv){
//   //     if (m_bContainsMultiGroupPrefillSeq){
//   //         /// mmmmm pppp ddddd
//   //         int last_len = appendKey.size(0);
//   //         appendKey = appendKey.slice(0, m_nMultiGroupSeqPrefillLen,
//   //         last_len); appendValue = appendValue.slice(0,
//   //         m_nMultiGroupSeqPrefillLen, last_len);
//   //     }
//   //     else if (m_bContainsMultiGroupDecodeSeq){
//   //         /// pppp ddddd m
//   //         int last_len = appendKey.size(0);
//   //         appendKey = appendKey.slice(0, 0, last_len - 1);
//   //         appendValue = appendValue.slice(0, 0, last_len - 1);
//   //     }
//   // }

//   // auto appendKey = _appendKey.slice(0, 0, m_nNumPrefillTokens);
//   // auto appendValue = _appendValue.slice(0, 0, m_nNumPrefillTokens);

//   // Append kv cache
//   // AppendKVCache(appendKey, appendValue, kvCache);

//   int prefill_start_idx = 0;
//   int prefill_end_idx = m_nNumPrefillTokens;
//   int decode_start_idx = m_nNumPrefillTokens;
//   int decode_end_idx = m_nNumPrefillTokens + m_nNumDecodeTokens;
//   int multi_start_idx = 0;
//   int multi_end_idx = 0;

//   if (m_bContainsMultiGroupPrefillSeq)
//   {
//     multi_start_idx = 0;
//     multi_end_idx = m_nMultiGroupSeqPrefillLen;

//     prefill_start_idx = multi_end_idx;
//     prefill_end_idx = m_nMultiGroupSeqPrefillLen + m_nNumPrefillTokens;

//     decode_start_idx = prefill_end_idx;
//     decode_end_idx = q.size(0);
//   }
//   else if (m_bContainsMultiGroupDecodeSeq)
//   {

//     prefill_start_idx = 0;
//     prefill_end_idx = m_nNumPrefillTokens;

//     decode_start_idx = multi_end_idx;
//     decode_end_idx = q.size(0) - 1;

//     multi_start_idx = decode_end_idx;
//     multi_end_idx = q.size(0);
//   }

//   auto q_prefill = _q.slice(0, prefill_start_idx, prefill_end_idx);
//   auto q_decode = _q.slice(0, decode_start_idx, decode_end_idx);
//   auto q_multi = _q.slice(0, multi_start_idx, multi_end_idx);

//   if (m_bContainsMultiGroupPrefillSeq || m_bContainsMultiGroupDecodeSeq)
//   {
//     auto outputAndLse_Multi =
//         m_multi_group_wrapper.Forward(nSoftmaxScale, q_multi, kvCache);
//     output.slice(0, multi_start_idx, multi_end_idx) = outputAndLse_Multi[0];
//     S.slice(0, multi_start_idx, multi_end_idx) = outputAndLse_Multi[1];
//   }

//   if (m_nNumPrefillTokens)
//   {
//     auto outputAndLse_Prefill =
//         m_prefill_wrapper.Forward(nSoftmaxScale, q_prefill, kvCache);
//     output.slice(0, prefill_start_idx, prefill_end_idx) =
//         outputAndLse_Prefill[0];
//     S.slice(0, prefill_start_idx, prefill_end_idx) = outputAndLse_Prefill[1];
//   }

//   if (m_nNumDecodeTokens)
//   {
//     auto outputAndLse_Decode =
//         m_decode_wrapper.Forward(nSoftmaxScale, q_decode, kvCache);
//     output.slice(0, decode_start_idx, decode_end_idx) =
//     outputAndLse_Decode[0]; S.slice(0, decode_start_idx, decode_end_idx) =
//     outputAndLse_Decode[1];
//   }

//   if (m_prefill_wrapper.m_bSkipAttentionReduction)
//   {
//     output = output.reshape({-1, m_nNumQHeads * m_nHeadDim});
//     return output;
//   }

//   // Merge states
//   bool should_gather_tensor =
//       (!m_prefill_wrapper.m_bSkipAttentionReduction &&
//        (m_bContainsMultiGroupPrefillSeq || m_bContainsMultiGroupDecodeSeq));

//   if (should_gather_tensor)
//   {
//     output = m_multi_group_wrapper.GatherTensor(
//         output,
//         S,
//         m_bContainsMultiGroupPrefillSeq,
//         m_bContainsMultiGroupDecodeSeq,
//         m_nMultiGroupSeqPrefillLen,
//         m_vMultiGroupSeqGroupIds);
//   }

//   output = output.reshape({-1, m_nNumQHeads * m_nHeadDim});
//   return output;
// }
// //==============================================================================