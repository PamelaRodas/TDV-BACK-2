package com.tvd.backend.service;

import com.tvd.backend.dto.CreatePhotoMomentRequest;
import com.tvd.backend.model.PhotoMoment;
import com.tvd.backend.repository.PhotoMomentRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Service
public class PhotoMomentService {

    private final PhotoMomentRepository repository;

    public PhotoMomentService(PhotoMomentRepository repository) {
        this.repository = repository;
    }

    public List<PhotoMoment> getAllMoments() {
        return repository.findAll();
    }

    public PhotoMoment addMoment(CreatePhotoMomentRequest request) {
        String id = "photo-" + UUID.randomUUID();
        PhotoMoment moment = new PhotoMoment(
                id,
                request.getImage(),
                request.getCaption(),
                normalizeAuthor(request.getAuthor()),
                LocalDateTime.now()
        );
        return repository.save(moment);
    }

    private String normalizeAuthor(String author) {
        if (author == null || author.trim().isEmpty()) {
            return "anonymous soul";
        }
        return author.trim();
    }
}
