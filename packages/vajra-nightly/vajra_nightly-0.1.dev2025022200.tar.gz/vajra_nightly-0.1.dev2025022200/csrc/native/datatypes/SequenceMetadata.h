#pragma once

#include "Logging.h"
#include "StdCommon.h"
//==============================================================================
namespace vajra
{
//==============================================================================
class SequenceMetadata
{
public:
  SequenceMetadata(
      std::size_t nScheduleId,
      std::string& strSeqId,
      std::size_t nNumQTokens,
      std::size_t nNumKvTokens,
      std::vector<std::size_t>& vnBlockTable,
      std::vector<std::size_t>& vnKvpGroupIds,
      bool bSaveKvCache)
      : m_nScheduleId(nScheduleId),
        m_strSeqId(strSeqId),
        m_nNumQTokens(nNumQTokens),
        m_nNumKvTokens(nNumKvTokens),
        m_vnBlockTable(vnBlockTable),
        m_vnKvpGroupIds(vnKvpGroupIds),
        m_bSaveKvCache(bSaveKvCache),
        m_bIsKvpRequest(vnKvpGroupIds.size() > 1)
  {
  }

  std::string ToString() const
  {
    return fmt::format(
        "SequenceMetadata("
        "ScheduleId: {}, "
        "SeqId: {}, "
        "NumQTokens: {}, "
        "NumKvTokens: {}, "
        "KvpGroupIds: [{}], "
        "SaveKvCache: {}, "
        "IsKvpRequest: {})",
        m_nScheduleId,
        m_strSeqId,
        m_nNumQTokens,
        m_nNumKvTokens,
        fmt::join(m_vnKvpGroupIds, ", "),
        m_bSaveKvCache,
        m_bIsKvpRequest);
  }

  std::size_t m_nScheduleId;
  std::string m_strSeqId;
  std::size_t m_nNumQTokens;
  std::size_t m_nNumKvTokens;
  std::vector<std::size_t> m_vnBlockTable;
  std::vector<std::size_t> m_vnKvpGroupIds;
  bool m_bSaveKvCache;
  bool m_bIsKvpRequest;
};
//==============================================================================
} // namespace vajra
//==============================================================================