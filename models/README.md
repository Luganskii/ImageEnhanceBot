# Database Schema

## Tables

### User
| Column             | Type     | Constraints                        |
|--------------------|----------|------------------------------------|
| id                 | Integer  | Primary Key                        |
| subscription       | Integer  | Foreign Key (subscription.id), Not Null |
| language           | String(3)| Not Null, Default 'eng'            |
| balance            | Float    | Not Null, Default 0.0              |
| registration_date  | Date     | Not Null, Default Current Date     |

### SubscriptionHistory
| Column             | Type     | Constraints                        |
|--------------------|----------|------------------------------------|
| id                 | Integer  | Primary Key                        |
| user_id            | Integer  | Foreign Key (user.id), Not Null    |
| type_subscription  | Integer  | Foreign Key (subscription.id), Not Null |
| paid               | Float    | Not Null                           |

### Subscription
| Column             | Type     | Constraints                        |
|--------------------|----------|------------------------------------|
| id                 | Integer  | Primary Key                        |
| description        | String(100) | Not Null                        |
| price              | Float    | Not Null, Default 0.0              |

### Activity
| Column             | Type     | Constraints                        |
|--------------------|----------|------------------------------------|
| id                 | Integer  | Primary Key                        |
| day                | Date     | Not Null, Default Current Date     |
| user_id            | Integer  | Foreign Key (user.id), Not Null    |
| model              | String(10) | Foreign Key (models.id), Not Null |

### Models
| Column             | Type     | Constraints                        |
|--------------------|----------|------------------------------------|
| id                 | String(10) | Primary Key                      |
| count_of_params    | Integer  | Not Null                           |
| type               | String(10) | Not Null                         |

## Relationships

- **User** has many **SubscriptionHistory**
  - `User.id` -> `SubscriptionHistory.user_id`
- **User** has many **Activity**
  - `User.id` -> `Activity.user_id`
- **SubscriptionHistory** belongs to **User**
  - `SubscriptionHistory.user_id` -> `User.id`
- **SubscriptionHistory** belongs to **Subscription**
  - `SubscriptionHistory.type_subscription` -> `Subscription.id`
- **Subscription** has many **SubscriptionHistory**
  - `Subscription.id` -> `SubscriptionHistory.type_subscription`
- **Activity** belongs to **User**
  - `Activity.user_id` -> `User.id`
- **Activity** belongs to **Models**
  - `Activity.model` -> `Models.id`
- **Models** has many **Activity**
  - `Models.id` -> `Activity.model`
