package com.tvd.backend.exception;

public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String resource, String id) {
        super(String.format("%s with id '%s' was not found", resource, id));
    }
}
