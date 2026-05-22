package com.tvd.backend.repository;

import com.tvd.backend.model.PhotoMoment;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PhotoMomentRepository extends JpaRepository<PhotoMoment, String> {
}
