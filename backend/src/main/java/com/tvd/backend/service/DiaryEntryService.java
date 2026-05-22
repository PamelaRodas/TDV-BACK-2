package com.tvd.backend.service;

import com.tvd.backend.dto.CreateDiaryEntryRequest;
import com.tvd.backend.model.DiaryEntry;
import com.tvd.backend.repository.DiaryEntryRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Service
public class DiaryEntryService {

    private final DiaryEntryRepository repository;

    public DiaryEntryService(DiaryEntryRepository repository) {
        this.repository = repository;
    }

    public List<DiaryEntry> getAllEntries() {
        return repository.findAll();
    }

    public DiaryEntry addEntry(CreateDiaryEntryRequest request) {
        String id = "diary-" + UUID.randomUUID();
        DiaryEntry entry = new DiaryEntry(
                id,
                request.getTitle(),
                request.getText(),
                request.getLabel(),
                normalizeAuthor(request.getAuthor()),
                LocalDateTime.now()
        );
        return repository.save(entry);
    }

    private String normalizeAuthor(String author) {
        if (author == null || author.trim().isEmpty()) {
            return "anonymous soul";
        }
        return author.trim();
    }
}
