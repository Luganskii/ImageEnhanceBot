# Database Schema

## Tables

### Users
| Column             | Type     | Constraints                        |
|--------------------|----------|------------------------------------|
| id                 | Integer  | Primary Key                        |
| subscription_id    | Integer  | Foreign Key (subscription.id), Not Null |
| language           | String   | Not Null, Default 'eng'            |
| balance            | Double   | Not Null, Default 0.0              |
| registration_date  | Datetime | Not Null, Default Current Date     |

### PaymentsHistory
| Column             | Type     | Constraints                        |
|--------------------|----------|------------------------------------|
| id                 | Integer  | Primary Key                        |
| user_id            | Integer  | Foreign Key (user.id), Not Null    |
| subscription_id    | Integer  | Foreign Key (subscription.id), Not Null |
| paid               | Double   | Not Null                           |

### Subscriptions
| Column             | Type     | Constraints                        |
|--------------------|----------|------------------------------------|
| subscription_id    | Integer  | Primary Key                        |
| description        | String   | Not Null                        |
| price              | Double   | Not Null, Default 0.0              |

### Activities
| Column             | Type     | Constraints                        |
|--------------------|----------|------------------------------------|
| id                 | Integer  | Primary Key                        |
| date_time          | Datetime | Not Null, Default Current Date     |
| user_id            | Integer  | Foreign Key (user.id), Not Null    |
| model              | String   | Foreign Key (models.id), Not Null |

### Models
| Column             | Type     | Constraints                        |
|--------------------|----------|------------------------------------|
| id                 | String   | Primary Key                      |
| count_of_params    | Integer  | Not Null                           |
| type               | String   | Not Null                         |

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
