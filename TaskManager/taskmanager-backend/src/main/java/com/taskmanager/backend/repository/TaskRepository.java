package com.taskmanager.backend.repository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.taskmanager.backend.model.Task;

@Repository
public interface TaskRepository extends JpaRepository<Task, Long> {

}
