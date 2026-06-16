export interface FieldOption {
  value: string
  label: string
}

export interface FieldSpec {
  id: string
  label: string
  payload_key: string
  control_type: 'text' | 'number' | 'checkbox' | 'select'
  placeholder: string
  default: string | boolean
  help_text: string
  options: FieldOption[]
}

export interface ModuleSpec {
  id: string
  title: string
  description: string
  json_endpoint: string
  image_endpoint: string
  requires_target: boolean
  default_target_key: 'bnet_id' | 'customer_token'
  fields: FieldSpec[]
}

export interface BootstrapPayload {
  default_module_id: string
  modules: ModuleSpec[]
}

export interface ImageResultItem {
  url: string
  title: string
}

export type RequestStatus = 'idle' | 'loading' | 'success' | 'error'
