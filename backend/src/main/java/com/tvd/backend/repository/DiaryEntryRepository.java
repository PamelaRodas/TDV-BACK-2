package com.tvd.backend.repository;

import com.tvd.backend.model.DiaryEntry;
import org.springframework.data.jpa.repository.JpaRepository;

public interface DiaryEntryRepository extends JpaRepository<DiaryEntry, String> {
}
