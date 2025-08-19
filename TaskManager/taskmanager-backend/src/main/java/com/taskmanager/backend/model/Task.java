package com.taskmanager.backend.model;

import java.time.LocalDate;

import jakarta.persistence.*;

@Entity
public class Task {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;
	
	private String taskTitle;
	private LocalDate deadline;
	
	@Enumerated(EnumType.STRING)
	private Priority priority_level;
	
	@Enumerated(EnumType.STRING)
	private Status current_status;
	
	public enum Priority { LOW, MEDIUM, HIGH }
	public enum Status { COMPLETED, PENDING, DOING	 }
	
	public Long getId() {
	    return id;
	}

	public void setId(Long id) {
	    this.id = id;
	}
	
	public String getTaskTitle() {
		return taskTitle;
	}
	public void setTaskTitle(String taskTitle) {
		this.taskTitle = taskTitle;
	}
	public LocalDate getDeadline() {
		return deadline;
	}
	public void setDeadline(LocalDate deadline) {
		this.deadline = deadline;
	}
	
	public Priority getPriority() {
		return this.priority_level;
	}
	
	public void setPriority(Priority p) {
		this.priority_level = p;
	}
	
	public Status getStatus() {
		return this.current_status;
	}
	
	public void setStatus(Status s) {
		this.current_status = s;
	}
	
	
	

}
