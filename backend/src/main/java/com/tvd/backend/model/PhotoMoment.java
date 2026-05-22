package com.tvd.backend.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.LocalDateTime;

@Entity
@Table(name = "photo_moments")
public class PhotoMoment {
    @Id
    private String id;

    private String image;
    private String caption;
    private String author;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    public PhotoMoment() {
    }

    public PhotoMoment(String id, String image, String caption, String author, LocalDateTime createdAt) {
        this.id = id;
        this.image = image;
        this.caption = caption;
        this.author = author;
        this.createdAt = createdAt;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getImage() {
        return image;
    }

    public void setImage(String image) {
        this.image = image;
    }

    public String getCaption() {
        return caption;
    }

    public void setCaption(String caption) {
        this.caption = caption;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
