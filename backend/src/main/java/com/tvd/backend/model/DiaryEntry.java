package com.tvd.backend.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.LocalDateTime;

@Entity
@Table(name = "diary_entries")
public class DiaryEntry {
    @Id
    private String id;

    private String title;
    private String text;
    private String label;
    private String author;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    public DiaryEntry() {
    }

    public DiaryEntry(String id, String title, String text, String label, String author, LocalDateTime createdAt) {
        this.id = id;
        this.title = title;
        this.text = text;
        this.label = label;
        this.author = author;
        this.createdAt = createdAt;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public String getLabel() {
        return label;
    }

    public void setLabel(String label) {
        this.label = label;
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
