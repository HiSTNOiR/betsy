# Project Architecture

## Overview

Betsy Bot is a modular, event-driven Twitch bot built on a publish-subscribe architecture. The application is designed to be extensible, maintainable, and easy to understand, with complete decoupling between components.

## Core Principles

### 1. Pure Publish-Subscribe

All components communicate exclusively through events.

### 2. Single Responsibility

Each component performs exactly one function.

### 3. Complete Decoupling

Components have no direct dependencies on each other.

### 4. Thread-Safe Processing

Simultaneous connections to OBS, Twitch, Discord, YouTube, StreamElements, Spotify and any other platforms are handled appropriately.

### 5. Extensibility

New features can be added by creating new subscribers.

### 6. Testability

Components can be tested in isolation.

## System Architecture

### Event Bus

The central component is the event_bus, which manages all communication within the application. Components interact by:

- Publishing events to the bus
- Subscribing to events they need to process

No direct component-to-component calls exist, ensuring complete decoupling.

### Component Types

The application consists of four primary component types:

- Publishers (input sources that create events)
- Processors (transform events into new events)
- Subscribers (react to events and perform actions)
- Models (define data structures used in events)

### Data Flow

A typical data flow follows this pattern:

**Publishers** 👉 **Event Bus** 👉 **Processors** 👉 **Event Bus** 👉 **Subscribers** 👉 **Event Bus**

For example, here's a Twitch chat message:

`twitch_reader` publishes a `RawMessageReceived` event  
👇  
`sanitiser` processes it and publishes a `SanitisedMessageReceived` event  
👇  
`command_parser` processes it and publishes a `CommandReceived` event   
👇  
`command_handler` subscribes and processes the command  
👇  
`db_writer` persists any changes  
👇  
`twitch_sender` sends any response back to Twitch  

## User Interfaces

The system supports multiple interfaces:

- Twitch Chat (primary interface for users)
- Web Interface (dashboard for streamers [possibly expanding to end users TBD])
- Kivy App (desktop/mobile application for on-the-go management)

All interfaces publish and subscribe to the same event bus, ensuring consistent state across the system.

## Event Types

Key event types include:

- RawMessageReceived (new message from Twitch)
- CommandReceived (Command identified in a message)
- PointsUpdated (User points changed)
- DuelCompleted (duel has finished)
- DatabaseUpdated (data has been persisted)
- UiUpdateNeeded (UI needs to refresh data)

## Adding New Features

To add a new feature:

- Create new data models if needed
- Add publishers if the feature needs new input sources
- Add processors if the feature requires data transformation
- Add subscribers to handle the feature's business logic
- Update UI components to interact with the feature

## Testing Strategy

- Unit Tests (test individual components in isolation)
- Integration Tests (verify event flows through multiple components)
- End-to-End Tests (test complete workflows from input to output)
- UI Tests (verify UI components reflect system state correctly)